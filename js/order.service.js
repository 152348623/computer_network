var orderDataService = {
    sendOrder: sendOrder,
    getInquireOrder: getInquireOrder,
    cancelInquireOrder: cancelInquireOrder,
    getOrderIfSuccess: getOrderIfSuccess,
    getAllComment: getAllComment,
    sendCommentFOrOrder: sendCommentFOrOrder,
    removeComment: removeComment

}
var url = "https://10.106.10.161:5000/backend/"


// API

function sendOrder(orderData) {
    $.ajax({
        url: url + "sendOrder",
        type: "POST",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(orderData),
        success: function (data) {
            window.location.href = 'checkOrder.html';
        },
        error: function () {
            alert("Phone is exist or other error!")
        }
    });
}

function getInquireOrder(phone, onSuccess, onFailure) {
    $.ajax({
        url: url + "getInquireOrder?phone=" + phone,
        type: "GET",
        contentType: 'application/json; charset=UTF-8',
        success: onSuccess,
        error: onFailure
    });
}

function cancelInquireOrder(phone, onSuccess, onFailure) {
    $.ajax({
        url: url + "cancelInquireOrder",
        type: "POST",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(phone),
        success: onSuccess,
        error: onFailure
    });
}

function getOrderIfSuccess(onSuccess, onFailure) {
    $.ajax({
        url: url + "getOrderIfSuccess",
        type: "GET",
        contentType: 'application/json; charset=UTF-8',
        success: onSuccess,
        error: onFailure
    });
}

function getAllComment(onSuccess, onFailure) {
    $.ajax({
        url: url + "getAllComment",
        type: "GET",
        contentType: 'application/json; charset=UTF-8',
        success: onSuccess,
        error: onFailure
    });
}

function sendCommentFOrOrder(data, onSuccess, onFailure) {

    $.ajax({
        url: url + "sendCommentFOrOrder",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: onSuccess,
        error: onFailure
    });
}

function removeComment(data, onSuccess, onFailure) {
    $.ajax({
        url: url + "removeComment",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: onSuccess,
        error: onFailure
    });
}