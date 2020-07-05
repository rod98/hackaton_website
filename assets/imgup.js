window.onload = function () {
    document.getElementById("files").onchange = function () {
        var reader = new FileReader();

        reader.onload = function (e) {
            // get loaded data and render thumbnail.
            document.getElementById("preview").src = e.target.result;
        };

        // read the image file as a data URL.
        reader.readAsDataURL(this.files[0]);
        
        //document.getElementById("upload").style.visibility = "visible"
        //document.getElementById("upload").style.visibility = "visible"
        //document.getElementById("upload").style.display = "block"
        document.getElementById("upload").classList.remove("hidden");
    };
}