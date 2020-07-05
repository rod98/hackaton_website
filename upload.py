import os
import myutils as myu
from PIL import Image

def load(form):
    item = form['churchimg']
  
    # save a image using extension 
    #im1 = im1.save("geeks.jpg") 
    
    msg = ""
    # Test if the file was uploaded
    if item.filename:
        fn = "img/" + os.path.basename(item.filename)
        open (fn, 'wb').write(item.file.read())
        msg = fn
    else:
        msg = ''
        
    return msg

def azurimg(fname):
    import requests
    url = "https://churchvision.cognitiveservices.azure.com/customvision/v3.0/Prediction/28477bea-43d5-4abc-8c72-28795e697397/classify/iterations/Iteration6/image"

    image=fname
    
    image_f = Image.open(fname).convert("RGB")
    
    # image.width > 2000 or image.height > 2000 or
    if image_f.width * image_f.height > 3000 * 3000:
        image_f.thumbnail((3000, 3000))
        image_f.save(fname)
    
    payload = open(image, 'rb')
    headers = {
      'Prediction-key': 'ea9a13a62060437cbcaa48f97d708356',
      'Content-Type': 'application/octet-stream'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    return response

def gen_shame(response, catid):
    ret = ""
    
    if catid != "":
        jdata = response.json()
        
        catnm = ""
        ansid = jdata['predictions'][0]['tagId']
        for pred in jdata['predictions']:
            name = pred["tagName"]
            tgid = pred["tagId"]

            if tgid == catid:
                catnm = name
                break
            
        ret += "<p>You were asked to find a <b>" + catnm + "</b> building</p>"
        
        if ansid == catid:
            ret += "<div class='centered'>"
            ret += "<p class='correct'>"
            ret += "<span class='glorious'>GLORIOUS</span>"
            ret += "<br>"
            ret += "<span class='success'>SUCCESS</span>"
            ret += "</p>"
            ret += "</div>"
        else:
            ret += "<p class='incorrect'>Try better next time!</p><br>"
    
    return ret

def gen_tbl(response):
    ret = ""
    jdata = response.json()
    max_chance = 0
    
    # style='width: "+str(chance * 0.8)+"%;'
    
    tbl = "<table>"
    for pred in jdata['predictions']:
        chance = (pred['probability'] * 100);
        
        if chance > max_chance:
            max_chance = chance
        
        tbl += "<tr>"
        tbl += "<th class='lefter'>"
        tbl += "<div class='resback' style='width: "+str(chance)+"%;'>"
        tbl += pred['tagName'] + "</div>"
        tbl += "</th>"
        tbl += "<th class='righter'>" + ("%.2f" % chance) + "</th>"
        tbl += "</tr>"
        
    tbl += "</table>"
    
    ret += "Results:<br><hr>" + tbl
    
    if max_chance < 30:
        ret = "Sorry, but this doesn't look like a building."
    
    return ret 

def run(url, environ, start_response):
    start_response(b'200 OK', [(b'Content-Type', b'text/html')])

    import cgi
    
    msg   = "<div class='readable'>"
    fname = ""
        
    #form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)
    form = myu.get_form(environ)
    
    catid = ""
    try:
        fname = load(form)

        if fname != "":
            catid = myu.get_posttxt(form, "catid")

            resp = azurimg(fname)
            tbl  = gen_tbl (resp)
            
            if not "Sorry" in tbl:
                msg += gen_shame(resp, catid)
                
            msg += tbl
            #os.remove(fname)

    except Exception as inst:
        #msg += "<br>ERROR-1: " + str(inst)
        msg += "Error occured. Please try loading the file again!" + "<br>ERROR-1: " + str(inst)    
        
    msg += "</div>"
    
    if catid == "":
        msg += "<div><a href='pages/upload_image.html'><button>&#8592; Back</button></a></div>"
    else:
        msg += "<div><a href='pages/task.html'><button>&#8592; Back</button></a></div>"
        
    try:
        msg  = myu.get_insides("assets/header.html") + msg
        msg += myu.get_insides("assets/bottom.html")
    except Exception as inst:
        msg += "<br>ERROR-2: " + str(inst)
        
    return msg