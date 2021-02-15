import mechanize, verification, session

def call_this():
    response = session.check_aadhaar()
    #print(response)
    verification.check_exist(response)