function enab(pas, btn) {
    if (document.getElementById(pas).value === "")
        document.getElementById(btn).disabled = true
    else
        document.getElementById(btn).disabled = false
}

function reg(breg) {
    //document.getElementById("freg").style.visibility = "visible"
    //document.getElementById("freg").style.display    = "block"
    //document.getElementById("flog").style.visibility = "hidden"
    //document.getElementById("flog").style.display    = "none"
    
    if (breg) {
        document.getElementById("freg").classList.remove("hidden");
        document.getElementById("flog").classList.add   ("hidden");
        document.getElementById("swch").innerHTML = "Registered?"
        document.getElementById("swch").onclick   = function() { reg(0); }
    }
    else {
        document.getElementById("freg").classList.add   ("hidden");
        document.getElementById("flog").classList.remove("hidden");
        document.getElementById("swch").innerHTML = "No account?"
        document.getElementById("swch").onclick   = function() { reg(1); }
    }
}

function chpass() {
    pass1 = document.getElementById("opswrd").value
    pass2 = document.getElementById("dbpswrd").value
    
    if (pass1 == pass2 && pass1 !== "" && pass2 !== "") 
        //document.getElementById("Register").classList.add("disabled")
        document.getElementById("Register").disabled = false
    else
        document.getElementById("Register").disabled = true
}