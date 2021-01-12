
// success and failure

function onSuccess(data) {
    var $number = $('#number');
    var $date = $('#datepicker');
    var $hour = $('#hours');
    var $minute = $('#minutes');
    var $person = $('#persons');
    $number.html(data.phone);
    $date.html(data.date);
    $hour.html(data.hour);
    $minute.html(data.minute);
    $person.html(data.person);
}

function onFailure() {
  alert("order error");
}

// ready

$(document).ready(function () {

  orderDataService.getOrderIfSuccess(onSuccess, onFailure);
});