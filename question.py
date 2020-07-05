import myutils as myu 
import random

def run(url, env, start_response):
    start_response(b'200 OK', [(b'Content-Type', b'text/html')])
    
    result  = ""
    result += myu.get_insides("assets/header.html")
    result += "<form action='/answer.py'  method='post' enctype='multipart/form-data'>"
    result += "<div class='readable'>"
    
    try:
        conn = myu.get_conn()
        cu1  = conn.cursor()
        
        cu1.execute("SELECT TOP 1 * FROM questions_answers ORDER BY NEWID()")

        for row in cu1:
            quid    = myu.get_sqlval(row, 0)
            result += myu.get_sqlval(row, 1) + "<br><hr/>"
            #result += myu.get_sqlval(row, 4) + "<br>"
            
            catid = myu.get_sqlval(row, 2)
            truid = myu.get_sqlval(row, 3)
            #result += myu.get_sqlval(str(row), 3) + "<br>"
            #result += "<hr/>" + str(row) + "<br>"
        
            all_ans = []
            cu_answ = myu.get_conn().cursor()
            cu_anst = myu.get_conn().cursor()
            cu_answ.execute("SELECT TOP 3 * FROM answers WHERE id_category = " + catid + " AND NOT id = " + truid + " ORDER BY NEWID()")
            cu_anst.execute("SELECT * FROM answers WHERE id = " + truid)
            
            for row_ans in cu_anst:
                all_ans.append({"txt": myu.get_sqlval(row_ans, 1), "id": myu.get_sqlval(row_ans, 0)})
                
            for row_ans in cu_answ:
                all_ans.append({"txt": myu.get_sqlval(row_ans, 1), "id": myu.get_sqlval(row_ans, 0)})
                
            random.shuffle(all_ans)
            for ans in all_ans:
                result += "<input type='radio' id='" + str(ans["id"]) + "' name='ans_id' value='" + str(ans["id"]) + "'>"
                result += "<label for='" + str(ans["id"]) + "'>" + str(ans["txt"]) + "</label><br>"
                #result += "<br>" + str(ans["txt"])
                
            result += "<br>"
            result += "<input style='display: none;' id='answer' type='text' value='"+quid+"' name='que_id'>"
                
    except Exception as inst:
        result += "<br>ERROR-1: " + str(inst)
    
    result += "</div>"
    result += "<div class='centered'>"
    result += "<input id='answer' type='submit' value='Answer' name='submit'>"
    result += "</div>"
    result += "</form>"
    result += myu.get_insides("assets/bottom.html")
    
    return result