import requests
import os
import json


def ocr_space_file(filename, overlay=True, api_key='76d615781788957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    # print("Json",r.json(),type(r.json()))
    return r.json()
    # return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='76d615781788957', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )


def driving_license(arr,n):
    dl_no=doe=doi=name=""
    try:
        for i in range(0,n):
            if "Dt No" in arr[i]["LineText"] or "DL No" in arr[i]["LineText"]:
                dl_no=arr[i]["LineText"]
            if "valid Till" in arr[i]["LineText"]:
                doe=arr[i]["LineText"]

            if "DO" in arr[i]["LineText"] and doi!="":
                doi=arr[i]["LineText"]

            if "Name" in arr[i]["LineText"]:
                name=arr[i]["LineText"]
        print(dl_no[5:],doi,doe[10:-3],name[5:])
        details={"dl_no":dl_no[5:],"date_of_issue":doi,"date_of_expiry":doe[10:-3],"name":name[5:]}
        return details
    except Exception as e:
        return None
    # for i in arr.keys():
    #     if "Dt No" in arr[i]["LineText"]:
    #         print(arr[i]["LineText"])


def aadhar(arr,n):
    # flag=0
    # aadhar_no = "" 
    # for i in range(0,n):
    #     print(arr[i]['LineText'],)
    #     if "Male" in arr[i]['LineText'] or "Female" in arr[i]['LineText'] or 'Mule' in arr[i]['LineText']:
    #         flag=1
    #     if flag==2:
    #         aadhar_no=arr[i]['LineText']
    #         break
    #     if flag==1:
    #         flag=2
    #print("aadhar no",aadhar_no)
    return {'name':arr[0]['LineText'],"aadhar":arr[3]['LineText']}


def pancard(arr,n):
    pancard_no=name=""
    flag=0 
    for i in range(0,n):
        print(arr[i]['LineText'])
        if i==1:
           name=arr[i]['LineText']
        if "Permanent" in arr[i]['LineText'] or "Account" in arr[i]['LineText']:
            # print("yeahd",arr[i]['LineText'])
            flag=1
        if flag==2:
            pancard_no=arr[i]['LineText']
            # print("Asdasd",pancard_no)
            break
        if flag==1:
            flag=2
    details={"name":name,"pancard_no":pancard_no}        
    print("pancard no",pancard_no)
    return details            


def main(verification_type,file_path):
    test_file = ocr_space_file(filename=file_path)
    try:
        arr=test_file['ParsedResults'][0]['TextOverlay']['Lines']
    except Exception as e:
        return None
    n=len(arr)
    if verification_type=="aadhar":
        return aadhar(arr,n)
    elif verification_type=="pancard":
        return pancard(arr,n)
    elif verification_type=="driving_license":
        return driving_license(arr,n)

# test_file = ocr_space_file(filename='pancard.jpeg')
# arr=test_file['ParsedResults'][0]['TextOverlay']['Lines']
# n=len(arr)
# pancard(arr,n)


























# Use examples:
# print(os.listdir())


# print(test_file)
# test=json.dumps(test_file) #, sort_keys=True,indent=4, separators=(',', ': '))
# test1=json.loads(test)
# test1=dict(test1)
#print((type(test1)))
# print(test)
# print(test_file)
# test_url= ocr_space_url(url='example_image.jpeg')
#print(test_url)
# print(test_url.index('Dt No'))

# for i in range(0,len(arr)):
#     print(arr[i])