import myutils as myu
import pyodbc 

def run(url, environ, start_response):
    start_response(b'200 OK', [(b'Content-Type', b'text/html')])
    
    result  = ""
    result += myu.get_insides("assets/header.html")
    result += "<div class = 'readable'>"
    
    form    = myu.get_form(environ)
    result += myu.get_posttxt(form, "catid")
    #result += myu.get_posttxt(environ, "blahblah")
    result += myu.get_posttxt(form, "tst1")
    result += myu.get_posttxt(form, "tst2")
    

    result += "</div>"
    result += myu.get_insides("assets/bottom.html")
                
    return result