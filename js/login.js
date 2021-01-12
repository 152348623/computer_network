
//Success and failure

function userLoginSuccess(data) {
    localStorage.setItem("userInfo", JSON.stringify(data));
    location.href = "index.html";
  }
  
  function userLoginFailure() {
    alert("user login fail")
  }
  
  // ready
  
  $(document).ready(function () {
  
    var btnLogin = document.getElementById('btnLogin');
  
    btnLogin.onclick = function () {
        var $email = document.getElementById('email').value;
        var $password = document.getElementById('password').value;
        var parm = {
            "email": $email,
            "password": $password
        }
      orderDataService.userLogin(parm, userLoginSuccess, userLoginFailure)
    }
  });