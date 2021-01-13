import psycopg2
from flask import Flask, request, Response, jsonify
import json
from flask_cors import CORS, cross_origin
import datetime
from google.cloud import firestore
import requests
app = Flask(__name__)
# CORS(app)
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
databaseIP = "10.104.10.167"
# databaseIP = "192.168.2.105"
# databaseIP = "127.0.0.1"
cors = CORS(app, resources={
    r"/backend/": {"origins": "https://" + databaseIP + ":5000"}})
app.config['DEBUG'] = True
connection = psycopg2.connect(database="network_computer",
                              user="admin", password="admin", host=databaseIP, port="5432")
cur = connection.cursor()

@app.route('/')
def run():
    return 'My Flask App!'

@app.route("/backend/userLogin", methods=['POST'])
@cross_origin(origin='*', headers=['Content- Type'])
def userLogin():
    accountData = request.get_json()
    firebaseSingInAPI = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + \
        'AIzaSyBSx_sJAvz0AmmffTDwODGAioXfyqP4Foc'
    header = {
        "Accept": "application/json"
    }
    print("aaa", accountData)
    parameters = {
        'email': accountData['email'],
        'password': accountData['password'],
        'returnSecureToken': True
    }
    try:
        r = requests.post(
            firebaseSingInAPI, data=parameters, headers=header)

        resp = json.loads(r.text)

        if 'error' not in resp:
            return jsonify({'idToken': resp['idToken'], 'name': get_user_info_by_email(accountData['email'])})
        else:
            error = resp['error']['message']
            if error == "INVALID_PASSWORD":
                error = "密碼錯誤"
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error:
                error = "請稍後再試"
            elif error == "EMAIL_NOT_FOUND":
                error = "此帳號不存在"

            return {'error': error}, 404,
    except Exception as e:
        print(e)


def get_user_info_by_email(email):

    users = {'wei.141227@gmail.com': 'wei', 't106590039@gmail.com': '哈哈是我啦'}
    return users[email]


@app.route("/backend/sendOrder", methods = ['POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def sendOrder():
    orderData = request.get_json()
    print("AAA order", orderData)
    try:
        cur.execute("INSERT into orders values((SELECT MAX( order_id )+1 FROM orders), %s, %s, %s, %s, %s)", (orderData["number"], orderData["date"], orderData["hour"], orderData["minute"], orderData["person"]))
        connection.commit()
        return jsonify({"orderData":orderData})
    except (Exception, psycopg2.DatabaseError) as error:
        cur.execute("rollback")
        return Response(
            "sendOrder fail",
            status=400
        )
    


@app.route("/backend/getInquireOrder", methods = ['GET'])
@cross_origin(origin='*',headers=['Content- Type'])
def getInquireOrder():
    # accountData = request.get_json()
    phone = request.args.get("phone")
    print("aaa phone ", phone)
    # print(accountData)
    cur.execute("SELECT * from orders where phone=%s", [phone])
    rows = cur.fetchall()
    print("rows", rows)
    if(len(rows) > 0):
        return jsonify({
            'id': rows[0][0],
            'phone': rows[0][1],
            'date': rows[0][2],
            'hour': rows[0][3],
            'minute': rows[0][4],
            'person': rows[0][5]
            })
    else:
        return Response(
            "getInquireOrder fail",
            status=400
        )

@app.route("/backend/cancelInquireOrder", methods = ['POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def cancelInquireOrder():
    orderData = request.get_json()

    try:
        cur.execute("DELETE from orders where phone=%s", [orderData["phone"]])
        connection.commit()
        return jsonify({"cancelOrder": True})
    except (Exception, psycopg2.DatabaseError) as error:
        # connection.commit()
        cur.execute("rollback")
        return Response(
            "cancel fail",
            status=400
        )

@app.route("/backend/getOrderIfSuccess", methods=['GET'])
@cross_origin(orgin='*', headers=['Content-Type'])
def getOrderIfSuccess():
    # try:
    cur.execute("SELECT * from orders where order_id=(SELECT MAX(order_id) from orders)")
    rows = cur.fetchall()
    print(rows)
    return jsonify({
        'id': rows[0][0],
        'phone': rows[0][1],
        'date': rows[0][2].strftime('%Y-%m-%d'),
        'hour': rows[0][3],
        'minute': rows[0][4],
        'person': rows[0][5]
        })
    # except (Exception, psycopg2.DatabaseError) as error:
        # connection.commit()
        # cur.execute("rollback")

        # return Response(
        #     "getOrderIfSuccess fail",
        #     status=400
        # )
    
@app.route("/backend/getAllComment", methods=['GET'])
@cross_origin(orgin='*', headers=['Content-Type'])
def getAllComment():
    cur.execute("SELECT * from comments")
    rows = cur.fetchall()
    print(rows)
    commentsList = []
    for i in range(len(rows)):
        commentInfo = {
            "userName": rows[i][0],
            "description": rows[i][1]
        }
        commentsList.append(commentInfo)
    
    return jsonify({"comments": commentsList})

@app.route("/backend/sendCommentFOrOrder", methods=['POST'])
@cross_origin(orgin='*', headers=['Content-Type'])
def sendCommentFOrOrder():

    commentData = request.get_json()

    cur.execute("INSERT into comments values(%s, %s)", (commentData["userName"], commentData["description"]))
    # rows = cur.fetchall()
    connection.commit()

    return jsonify({"addComment": True})

@app.route("/backend/removeComment", methods=['POST'])
@cross_origin(orgin='*', headers=['Content-Type'])
def removeComment():

    commentData = request.get_json()

    try:
        cur.execute("DELETE from order_comment where description=%s", [commentData["description"]])
        connection.commit()
        return jsonify({"cancelOrder": True})
    except (Exception, psycopg2.DatabaseError) as error:
        # connection.commit()
        cur.execute("rollback")
        return Response(
            "cancel fail",
            status=400
        )


@app.route("/storeToken", methods=['POST'])
@cross_origin(orgin='*', headers=['Content-Type'])
def storeToken():

    userInfoData = request.get_json()
    cur.execute("INSERT into token values(%s, %s)", (userInfoData["idToken"], userInfoData["name"]))
    # rows = cur.fetchall()
    connection.commit()

    return Response(
            "OK",
            status=200
        )

@app.route("/getAllToken", methods=['GET'])
@cross_origin(orgin='*', headers=['Content-Type'])
def getAllToken():
    cur.execute("SELECT * from token")
    rows = cur.fetchall()
    print(rows)
    tokenList = []
    for i in range(len(rows)):
        tokenInfo = {
            "token": rows[i][0],
            "userName": rows[i][1]
        }
        tokenList.append(tokenInfo)
    
    return jsonify({"token": tokenList})


if __name__ == "__main__":
    app.debug = True
    app.run(host= databaseIP, ssl_context ='adhoc' )
    # app.run(host= databaseIP)
