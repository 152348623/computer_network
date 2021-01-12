
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
        var userInfo = localStorage.getItem("userInfo");
        if (userInfo != null) {
            userInfo = JSON.parse(userInfo);
            var escapeData = escapeHTML(document.getElementById('userComment').value);
            var parm = { "userName": userInfo.name, "description":  escapeData }
            // console.log('AAA document.getElementById(userComment).innerText', document.getElementById('userComment').textContent);
            // var parm = {"userName": userInfo.name, "description":  document.getElementById('userComment').textContent }
            orderDataService.sendCommentFOrOrder(parm, sendCommentSuccess, sendCommentFailure);
        }
        else{
            alert("必須要登入才可留言")
        }

    }
});