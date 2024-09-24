function radio() {
    var radios = document.querySelector('#student');
    if (radios.checked) {
        document.querySelector("#grade").style.display= "inline";
    }else{
        document.querySelector("#grade").style.display= "none";
    }};
