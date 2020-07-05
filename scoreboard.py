import myutils as myu

def run(url, env, start_response):
    start_response(b'200 OK', [(b'Content-Type', b'text/html')])
    
    uid = myu.get_cookie(env, 'id')
    psw = myu.get_cookie(env, 'passwd')

    cu = myu.get_conn().cursor()
    cu.execute("SELECT name,e,series FROM usersdata WHERE id = '" + (uid) + "' AND pass_word = '" + (psw) + "'")
    
    msg  = myu.get_insides("assets/header.html")
    msg += "<div class='readable'>"
    
    if cu.rowcount != 0:
        row  = cu.fetchone()
        nm = myu.get_sqlval(row, 0)
        sc = myu.get_sqlval(row, 1)
        st = myu.get_sqlval(row, 2) 
        
        msg += "<b>You are: </b>" + nm + "<br>"
        msg += "<b>Score: </b>"   + sc + "<br>"
        msg += "<b>Strike: </b>"  + st + "<br>"
        
        cu.execute("SELECT COUNT(id) FROM usersdata WHERE e > " + sc)
        plc = 0
        if cu.rowcount != 0:
            cnt = cu.fetchone()
            plc = int(myu.get_sqlval(cnt, 0))
            
        msg += "<b>Your place: </b>" + str(plc + 1) + "<br>"
        
    try:
        cu.execute("SELECT TOP 10 name,e,series FROM usersdata ORDER BY e DESC")

        msg += "<br>"
        msg += "<table>"
        msg += "<tr class='header'>"
        msg += "<th class='header'>Name</th>"
        msg += "<th class='header'>Score</th>"
        msg += "<th class='header'>Strike</th>"
        msg += "</tr>"
        for row in cu:
            msg += "<tr>"
            
            msg += "<th>"
            msg += myu.get_sqlval(row, 0)
            msg += "</th>"
            
            msg += "<th>"
            msg += myu.get_sqlval(row, 1)
            msg += "</th>"
            
            msg += "<th>"
            msg += myu.get_sqlval(row, 2)
            msg += "</th>"
            
            msg += "</tr>"

        msg += "</table>"
    except Exception as inst:
        msg += "<br>ERROR: " + str(inst)
    
    msg += "</div>"
    msg += myu.get_insides("assets/bottom.html")
        
    return msg