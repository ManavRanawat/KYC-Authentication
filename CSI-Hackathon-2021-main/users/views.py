from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import KYC
from django.http import HttpResponse
from PIL import Image
from .ocr_latest import main
from .session import call1,call2
from users.opencv_face import crop_image
from .Kyc_face import verify as vf
from .api_calls import location_reveal,send_otp
import requests
from django.conf import settings
br = []
otp = ""
ip_addr=set()
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def verification(request):
    verified_documents=KYC.objects.get(user=request.user)
    fields= ['aadhar','pan','voter_card','passport','driving_license']

    return render(request, 'users/verification.html',{"verified_documents":verified_documents})

def upload_documents(request,doctype):
    return HttpResponse("<p>"+doctype+"</p>")


def checkValidity(S,num,request):
    encoded_num=S[3]
    # global ip_addr
    # print('IP HERE:',ip_addr)
    # if len(ip_addr)>1:
    #     return None
    num=str(num)
    if num[-3:]!=encoded_num[-3:]:
        return False
    city,state = location_reveal(request)
    if state.lower()!=S[2].lower():
        return False
    return True

@login_required
def aadhar_verify(request):
    global br   
    global ip_addr
    if request.method=="POST":
        ip = location_reveal(request)[2]
        print("IP:",ip)
        ip_addr.add(ip)
        number = request.POST['number']
        captcha = request.POST['captcha']
        print(request.FILES)
        picture = request.FILES['aadhar_id']
        image = Image.open(picture)
        print(image)
        print(type(picture))
        image.save('users/aadhar.jpeg')
        
        # ip = location_reveal(request)[2]
        # print("IP:",ip)
        # ip_addr.add(ip)
        #OCR
        aadhar_number = main('aadhar','users/aadhar.jpeg')['aadhar']
        print(len(aadhar_number))
        aadhar_number = ''.join(aadhar_number.split(" "))
        print("FINAL",aadhar_number)
        #Scraping
        # ip = location_reveal(request)[2]
        # print("IP:",ip)
        # ip_addr.add(ip)
        Flag,S = call2(aadhar_number,captcha,br)
        print(S)

        if Flag:

        #face verify
            val = vf(crop_image('users/aadhar.jpeg'),request.user.username)
            name=""
            isVerified = checkValidity(S,number,request)
            if isVerified != None:
                if val!='Unknown':# and isVerified:
                    name=val
                    print("name:",val)
                    #send otp to the users
                    phone_num="+91"+str(number)
                    global otp
                    otp = send_otp(phone_num)
                    messages.success(request, f'Your document has been verified successfully')
                    return redirect('otp-verify')
                else:
                    messages.error(request, f'Your face did not match with your aadhar card..Try again!')
                    return redirect('verification')
                    #return redirect()
            else:
                messages.error(request, f'You cannot bypass security!')
                return redirect('verification')
        else:
            messages.error(request, f'Your captcha/aadhar card is not valid!')
            return redirect('verification')

        
        
        return HttpResponse('<p>Yay</p>')

    else:
        # call to get captcha image
        br = call1()
        form = AadharVerificationForm()
        return render(request,"users/upload_document.html",{"form":form})

@login_required
def pan_verify(request):
    if request.method=="POST":

        #captcha = request.POST['captcha']
        print(request.FILES)
        picture = request.FILES['pancard']
        image = Image.open(picture)
        print(image)
        print(type(picture))
        image.save('users/pancard.jpeg')
        
        #OCR
        details = main('pancard','users/pancard.jpeg')
        pname = details["name"]
        pno = details["pancard_no"]

        # send to gosar API
        flag=False
        link = settings.DUMMY_API_LINK+"pancard"
        print("LINK:",link)
        getAPIdata = requests.get(url=link).json()
        #print(getAPIdata,"    ->",details)
        for oneuser in getAPIdata:
            #print(''.join(details["dl_no"].split(" ")),''.join(oneuser["dl_no"].split(" ")))
            if ''.join(details["pancard_no"].split(" ")) == ''.join(oneuser["pancard_no"].split(" ")):
                #print(details,"       ---------   ",oneuser)
                flag=True
                break
        if flag:

        #face verify
            val = vf(crop_image('users/pancard.jpeg'),request.user.username)
            name=""
            if val!='Unknown':
                name=val
                print("name:",val)
                #send otp to the users
                print("SUCCESS")
                #update in database
                KYC.objects.filter(user=request.user).update(pan=True)
                messages.success(request, f'Your pan card has been verified!')
                return redirect('verification')
            else:
                messages.error(request, f'Your face did not match with your pan card..Try again!')
                return redirect('verification')
        else:
            messages.error(request, f'Your Pan Card was not verified.')
            return redirect('verification')
            #return redirect()

        
        
        return HttpResponse('<p>Yay</p>')

    else:
        # call to get captcha image
        #global br
        #br = call1()
        form = PanVerificationForm()
        return render(request,"users/upload_other.html",{"form":form,"document":"Pan Card"})

@login_required
def driving_verify(request):
    if request.method=="POST":

        #captcha = request.POST['captcha']
        print(request.FILES)
        picture = request.FILES['driving_license']
        image = Image.open(picture)
        print(image)
        print(type(picture))
        image.save('users/driving_license.jpeg')
        
        #OCR
        details = main('driving_license','users/driving_license.jpeg')
        if details ==None:
            messages.error(request, f'Server error..Try again!')
            return redirect('verification')
        # pname = details["name"]
        # pno = details["pancard_no"]

        # send to gosar API
        flag=False
        link = settings.DUMMY_API_LINK+"driving_license"
        print("LINK:",link)
        getAPIdata = requests.get(url=link).json()
        #print(getAPIdata,"    ->",details)
        for oneuser in getAPIdata:
            i = details["dl_no"].find("M")
            det = ''.join(details["dl_no"][i:].split(" "))
            i = oneuser["dl_no"].find("M")
            userdet = ''.join(oneuser["dl_no"][i:].split(" "))
            print(det,userdet)
            if det == userdet:
                #print(details,"       ---------   ",oneuser)
                flag=True
                break
        if flag:
        #face verify
            val = vf(crop_image('users/driving_license.jpeg'),request.user.username)
            name=""
            if val!='Unknown':
                name=val
                print("name:",val)
                #send otp to the users
                print("SUCCESS")
                #update in database
                KYC.objects.filter(user=request.user).update(driving_license=True)
                messages.success(request, f'Your driving license has been verified!')
                return redirect('verification')
            else:
                messages.error(request, f'Your face did not match with your driver licence..Try again!')
                return redirect('verification')
                #return redirect()
        else:
            messages.error(request, f'Your Driver License was not verified.')
            return redirect('verification')
        
        
        return HttpResponse('<p>Yay</p>')

    else:
        # call to get captcha image
        #global br
        #br = call1()
        form = DrivingVerificationForm()
        return render(request,"users/upload_other.html",{"form":form,"document":"Driving License"})



def otp_verify(request):
    if request.method == 'POST':
        actual_otp = request.POST["otp"]
        global otp
        if str(actual_otp) == str(otp):
            print("SUCCESS")
            #update in database
            KYC.objects.filter(user=request.user).update(aadhar=True)
            messages.success(request, f'Your aadhar card has been verified!')
            return redirect('verification')

        else:
            print("GALAT",otp)
            messages.error(request, f'Your OTP seems to be wrong! You have to repeat the process..Sorry!')
            return redirect('verification')
    else:
        form = OtpForm()
        return render(request,"users/otp_form.html",{"form":form})
