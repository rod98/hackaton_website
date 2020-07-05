import requests

import myutils as myu

def run(url, environ, start_response):
    #start_response(b'200 OK', [(b'Content-Type', b'text/html')])

    import cgi
    
    header_set = False
    
    #msg   = "<div class='readable'>"
    fname = ""
    
    try:
        aurl = "https://churchvision.cognitiveservices.azure.com/customvision/v3.2/training/projects/28477bea-43d5-4abc-8c72-28795e697397/tags/"

        payload  = {}
        headers = {
          'Training-key': '7630079c9a174152891e9d30bc6a2649'
        }

        msg = str(requests.request("GET", aurl, headers=headers, data = payload).json())[1:][:-1].replace("'", '"').replace("None", '"none"')

    except Exception as inst:
        msg += str(inst)
        
    #msg += "</div>"
    
    #try:
    #    msg  = myu.get_insides("assets/header.html") + msg
    #    msg += myu.get_insides("assets/bottom.html")
    #except Exception as inst:
    #    msg += "<br>ERROR-2: " + str(inst)
        
    if not header_set:
        start_response(b'200 OK', [(b'Content-Type', b'text/html')])
        
    return msg

