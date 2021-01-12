$(document).ready(function () {

    var url = "http://10.106.10.161:5000/backend/"

    var btnSubmit = document.getElementById('btnSubmit');
    var num;
    btnSubmit.onclick = function () {
        var number = document.getElementById('number').value;
        var date = document.getElementById('datepicker').value;
        var hour = document.getElementById('hours').value;
        var minute = document.getElementById('minutes').value;
        var person = document.getElementById('persons').value;

        num = number;
        var orderData = {
            number: number,
            date: date,
            hour: hour,
            minute: minute,
            person: person
        }

        orderDataService.sendOrder(orderData);

    }
});