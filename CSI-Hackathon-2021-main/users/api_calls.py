import requests
from django.conf import settings
from boltiot import Sms
import random
def location_reveal(request):
    ip_addr = request.META.get("HTTP_X_FORWARDED_FOR")
    api_call = "http://ipinfo.io/"+str(ip_addr)+"?token="+str(settings.LOCATION_API_TOKEN)
    data = requests.get(api_call).json()
    city = data["city"]
    state = data["region"]
    return city,state,ip_addr
    
def generate_otp():
    return random.randint(100000,999999)

def send_otp(receiver_no):
    # client = Client(account_sid=settings.ACCOUNT_SID,)
    sms = Sms(settings.ACCOUNT_SID,settings.ACCOUNT_TOKEN,receiver_no,settings.TWILIO_PHONE_NUM)
    otp = generate_otp()
    otp_msg="Welcome to MuJrAA Decoders Tech.\nYour One Time Password(OTP) is "+str(otp)+" for document verification."
    sms.send_sms(otp_msg)
    print("SMS BHEJ TO DIYA>>AB TU BATA")
    return otp