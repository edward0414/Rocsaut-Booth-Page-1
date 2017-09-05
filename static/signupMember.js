function validatefName(){
    var re = /[A-Za-z -']$/;
    if(re.test(document.getElementById("fname").value)){
        document.getElementById("fname").style.background ='#ccffcc';
        return true;
    } else {
        document.getElementById("fname").style.background ='#ccffcc';
        document.getElementById("fname").style.bordercolor ='#DD2C00';
        return false; 
    }
} 


function validatelName(){
    var re = /[A-Za-z -']$/;
    if(re.test(document.getElementById("lname").value)){
        document.getElementById("lname").style.background ='#ccffcc';
        return true;
    } else {
        document.getElementById("lname").style.background ='#ccffcc';
        document.getElementById("lname").style.bordercolor ='#DD2C00';
        return false; 
    }
} 


function validateEmail(){
    var re = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/;
    if(re.test(document.getElementById("email").value)){
        document.getElementById("email").style.background ='#ccffcc';
        return true;
    } else {
        document.getElementById("email").style.background ='#ccffcc';
        document.getElementById("email").style.bordercolor ='#DD2C00';
        return false; 
    }
} 


function validatePhone(){
    var re = /[0-9]{10}]/;
    if(re.test(document.getElementById("phone").value)){
        document.getElementById("phone").style.background ='#ccffcc';
        return true;
    } else {
        document.getElementById("phone").style.background ='#ccffcc';
        document.getElementById("phone").style.bordercolor ='#DD2C00';
        return false; 
    }
} 