
//Success and failure

function getInquireOrderSuccess(data) {
  var $number = $('#number');
  var $date = $('#datepicker');
  var $hour = $('#hours');
  var $minute = $('#minutes');
  var $person = $('#persons');

  $number.html(data.phone);
  $date.html(new Date(data.date).toLocaleDateString());
  $hour.html(data.hour);
  $minute.html(data.minute);
  $person.html(data.person);

}

function getInquireOrderFailure() {
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

// ready

$(document).ready(function () {

  var btnInquire = document.getElementById('btnInquire');

  btnInquire.onclick = function () {
    var InquireNumber = document.getElementById('InquireNumber').value;
    orderDataService.getInquireOrder(InquireNumber, getInquireOrderSuccess, getInquireOrderFailure)

    // <script>
    //   firebase.database().ref("order").on("value", function(data){
    //     console.log("AAA", data)
    //   })
    // </script>

  }
});