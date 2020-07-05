import datetime 
import myutils as myu 

def set_cookie_header(name, value, days=365):
    dt = datetime.datetime.now() + datetime.timedelta(days=days)
    fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    secs = days * 86400
    return ('Set-Cookie', '{}={}; Expires={}; Max-Age={}; Path=/'.format(name, value, fdt, secs))

def handler(env, start_response):
    content_type = 'text/html'
    headers = [('Content-Type', content_type), set_cookie_header('id', '12', 1/24.0)]
    start_response('200 OK', headers)
    
def run(url, env, start_response):
    myu.cooker(start_response, 'id', '12', 1/24.0)
    
    result  = ""
    result += myu.get_insides("assets/header.html")
    result += myu.get_insides("assets/bottom.html")
    
    return result