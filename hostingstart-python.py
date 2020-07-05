import sys
import os.path
import platform
import myutils as myu
from urllib.parse import quote
import importlib

def application_orig(environ, start_response):
    start_response(b'200 OK', [(b'Content-Type', b'text/html')])

    with open ("index.html", "r") as hostingstart_file:
        hosting = hostingstart_file.read() 
        yield hosting.encode('utf8').replace(b'PYTHON_VERSION', platform.python_version().encode('utf8'))

def is_logged(env, url):
    logged = True
    
    if (".py" in url or ".html" in url or url == "") and (url != "login.py") and (url != "register.py"):
        logged = False
        uid = myu.get_cookie(env, 'id')
        psw = myu.get_cookie(env, 'passwd')

        cu = myu.get_conn().cursor()
        cu.execute("SELECT id FROM usersdata WHERE id = '" + (uid) + "' AND pass_word = '" + (psw) + "'")
        logged = False
        for row in cu:
            logged = True
            break

    return logged
        
def application(environ, start_response):
    result = ""
    url    = ""
    getq   = ""
    pstq   = ""
    
    #url += quote(environ.get('SCRIPT_NAME', ''))
    url += quote(environ.get('PATH_INFO', ''))
    url  = url[1:]
    
    if environ.get('QUERY_STRING'):
        getq += '?' + environ['QUERY_STRING']
        
    if not is_logged(environ, url):
        url = "pages/login.html"

    if ".py" in url:
        try:
            url = url.split('/')[-1][:-3]
            module = importlib.import_module(url)
            result = module.run(url, environ, start_response)
        except Exception as inst:
            start_response(b'200 OK', [(b'Content-Type', b'text/html')])
            result = str(inst)
        
    else:
        if ".css" in url:
            start_response(b'200 OK', [(b'Content-Type', b'text/css')])
        elif ".js" in url:
            start_response(b'200 OK', [(b'Content-Type', b'text/javascript')]) 
        else:
            start_response(b'200 OK', [(b'Content-Type', b'text/html')])

        #url = environ['wsgi.url_scheme']+'://'

        #if environ.get('HTTP_HOST'):
        #    url += environ['HTTP_HOST']
        #else:
        #    url += environ['SERVER_NAME']

        #    if environ['wsgi.url_scheme'] == 'https':
        #        if environ['SERVER_PORT'] != '443':
        #           url += ':' + environ['SERVER_PORT']
        #    else:
        #        if environ['SERVER_PORT'] != '80':
        #           url += ':' + environ['SERVER_PORT']


        if url == "/" or url == "":
            url = "index.html"

        fname = "./" + url

        if os.path.exists(fname):
            with open (fname, "r") as hostingstart_file:
                result += hostingstart_file.read() 
        else: 
            result = "<html>Error has occured! Url:"+url+"</html>"

    yield result.encode('utf8').replace(b'PYTHON_VERSION', platform.python_version().encode('utf8'))