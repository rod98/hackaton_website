import myutils as myu

def run(url, environ, start_response):
    #start_response(b'200 OK', [(b'Content-Type', b'text/html')])

    import cgi
    
    header_set = False
    
    msg   = "<div class='readable'>"
    fname = ""
        
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)
    
    try:
        lg = form['logname'].file.read().translate(str.maketrans({"'":  r"''"}))
        pw = form['passwrd'].file.read().translate(str.maketrans({"'":  r"''"}))
        
        #msg += str(lg) + "<br>"
        #msg += str(pw) + "<br>"
        
        #cu = myu.get_conn().cursor()
        
        #cu.execute("SELECT id FROM usersdata WHERE name = '" + (lg) + "' AND pass_word = '" + (pw) + "'")
        #cu.execute("SELECT * FROM usersdata WHERE id > 20")
        
        try:
            header_set = myu.usr_login(lg, pw, start_response)
        except Exception as inst:
            msg += "Error?<br>"
            
        msg += myu.gen_logmsg(header_set, lg)
            
    except Exception as inst:
        #msg += "<br>ERROR-1: " + str(inst)
        msg += "Error occured. A doggo died!" + "<br>ERROR-1: " + str(inst)
        
    msg += "</div>"
    #msg += "<div><a href='pages/login.html'><button>&#8592; Back</button></a></div>"
    try:
        msg  = myu.get_insides("assets/header.html") + msg
        msg += myu.get_insides("assets/bottom.html")
    except Exception as inst:
        msg += "<br>ERROR-2: " + str(inst)
        
    if not header_set:
        start_response(b'200 OK', [(b'Content-Type', b'text/html')])
        
    return msg