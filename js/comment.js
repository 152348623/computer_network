
// success and failure

function onSuccess(data) {
    var commentsList = data.comments;

    var addString = "";
    for (var i = 0; i < commentsList.length; i++) {
        addString +=
            "<div class=\"col-lg-12 col-md-11 col-xs-12 margin-div\">\
                <div\ class=\"row Philosophy-content\">\
                    <div class=\"col-lg-8 col-md-12 col-xs-12  resume\">\
                        <h4><b>大家都說:</h4>\
                        <h5 class=\"resume__description\" style=\"padding-left:10em;\">"
            + commentsList[i].description +
            "</h5>\
                    </div>\
                </div>\
            </div>"
    }

    var $contextComment = $('#context-comment');
    $contextComment.html(addString);
}

function onFailure() {
    alert("order error");
}


function sendCommentSuccess() {
    orderDataService.getAllComment(onSuccess, onFailure);
}

function sendCommentFailure() {
    alert("send comment fail")
}

$(document).ready(function () {

    orderDataService.getAllComment(onSuccess, onFailure);

    document.getElementById('btnSendComment').onclick = function () {
        var parm = { "description": document.getElementById('userComment').value }

        orderDataService.sendCommentFOrOrder(parm, sendCommentSuccess, sendCommentFailure);

    }
});