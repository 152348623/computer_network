//Success and failure

function getInquireOrderSuccess(data) {
  var $number = $('#number');
  var $date = $('#datepicker');
  var $hour = $('#hours');
  var $minute = $('#minutes');
  var $person = $('#persons');
  var canacelTrue = document.getElementById('btnCancelTrue');       // 取得確認取消資料

  $number.html(data.phone);
  $date.html(new Date(data.date).toLocaleDateString());
  $hour.html(data.hour);
  $minute.html(data.minute);
  $person.html(data.person);
  canacelTrue.value = "確認取消";
  console.log(canacelTrue.value);                                   // 顯示 確認取消
  // btnCancel.value = "";
}

function getInquireOrderFailure(){
  var $number = $('#number');
  var $date = $('#datepicker');
  var $hour = $('#hours');
  var $minute = $('#minutes');
  var $person = $('#persons');

  $number.html("查詢錯誤");
  $date.html("查詢錯誤");
  $person.html("查詢錯誤");
  $hour.html("XX");
  $minute.html("XX");
}

function cancelOrderSuccess(){
  window.location.href = 'cancelSuccess.html';
}

function cancelOrderFailure(){
  alert("取消訂位發生錯誤，可能是您輸入錯誤的訂位資訊")
}

// ready
$(document).ready(function () {
  var btnCancel = document.getElementById('btnCancel');             // 取得取消訂位資料
  var canacelTrue = document.getElementById('btnCancelTrue');       // 取得確認取消資料

  btnCancel.onclick = function () {                                 // 判斷取消定位是否按下
    var InquireNumber = document.getElementById('InquireNumber').value;

    orderDataService.getInquireOrder(InquireNumber, getInquireOrderSuccess, getInquireOrderFailure)
  }

  canacelTrue.onclick = function () {
    if (canacelTrue.value == "確認取消") {
      var InquireNumber = document.getElementById('InquireNumber').value;

      orderDataService.cancelInquireOrder({"phone": InquireNumber}, cancelOrderSuccess, cancelOrderFailure);

    }
  }
});