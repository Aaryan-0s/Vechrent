function hide(){
    var x=document.getElementById("pass");
    var y=document.getElementById("hide");
    var z=document.getElementById("unhide");

    if (x.type==="password"){
        x.type="text";
        y.style.display="none";
        z.style.display="block";
    }
    else{
        x.type="password";
        y.style.display="block";
        z.style.display="none";
    }


}


function hideup(){
    var x=document.getElementById("pass-signup");
    var y=document.getElementById("hide-signup");
    var z=document.getElementById("unhide-signup");

    if (x.type==="password"){
        x.type="text";
        y.style.display="none";
        z.style.display="block";
    }
    else{
        x.type="password";
        y.style.display="block";
        z.style.display="none";
    }


}


