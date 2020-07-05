document.addEventListener('readystatechange', event => { 
    if (event.target.readyState === "complete")
        load_home()
});

function load_home (e) {
    (e || window.event).preventDefault();

    fetch("avcats.py" /*, options */)
    .then((response) => response.text())
    .then((html) => {     
        var cat = (', ' + html).split(', {');
        
        cat = cat.filter(function(value, index, arr){ return !value.includes("Dio") })
        cat.shift()
        
        var catrow = cat[Math.floor(Math.random() * cat.length)];
        
        console.log(html + "\n\n")
        
        create_form('{' + catrow)
        
    })
    .catch((error) => {
        console.warn(error);
    });
}

function create_form(catrow) {
    console.log(catrow)
    
    const obj = JSON.parse(catrow);
    console.log(obj.id);
    
    //divobj = document.getElementById("content")
    
    /*divobj.innerHTML  = "Please load an image with a <b>" + obj.name + "</b> building:"
    divobj.innerHTML += "<form>"
    divobj.innerHTML += "<input value="+obj.id+" name='catid' class='hidden'></input>"
    divobj.innerHTML += "<input ></input>"
    divobj.innerHTML += "</form>"
    */
    
    document.getElementById("desc").innerHTML = "Please load an image with a <b>" + obj.name + "</b> building:"
    document.getElementById("catid").value = obj.id
    document.getElementById("content").classList.remove("hidden")
    document.getElementById("loading").classList.add("hidden")
    
    //obj.id + " " + obj.name;   
}