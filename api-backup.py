import psycopg2
from flask import Flask, request, Response, jsonify
import json
from flask_cors import CORS, cross_origin
import datetime
app = Flask(__name__)
# CORS(app)
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
databaseIP = "10.106.10.161"
cors = CORS(app, resources={r"/backend/": {"origins": "http://" + databaseIP + ":5000"}})
app.config['DEBUG'] = True
connection = psycopg2.connect(database="networkcomputer",
                              user="admin", password="sunbird", host=databaseIP, port="5432")
cur = connection.cursor()
# cur.execute("SELECT * from account where account_name=%s and account_password=%s", ("test", "test"))
# rows = cur.fetchall()
# if(len(rows) > 0):
#     print(rows)
# else:
#     print("NONONO")

@app.route('/')
def run():
    return 'My Flask App!'


@app.route("/backend/userLogin", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type'])

def userLogin():
    accountData = request.get_json()
    # print(accountData)
    cur.execute("SELECT account_id from account where account_name=%s and account_password=%s", (accountData['name'], accountData['password']))
    rows = cur.fetchall()
    if(len(rows) > 0):
        return jsonify({'id': rows[0][0]})
    else:
        return Response(
            "Login fail",
            status=400
        )

@app.route("/backend/getAllBookInfo")
@cross_origin(origin='localhost',headers=['Content- Type'])
def getAllBookInfo():
    # response = Flask.jsonify({'some': 'data'})
    
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # print(request)
    cur.execute("SELECT * from book")
    rows = cur.fetchall()
    # print(rows[0])
    bookInfoList = []
    for i in range(len(rows)):
        bookInfo = {
            "id": rows[i][0],
            "name": rows[i][1],
            "author": rows[i][2],
            "description": rows[i][3],
            "price": rows[i][4],
            "img": rows[i][5]
        }
        bookInfoList.append(bookInfo)
    
    return jsonify({"bookInfo": bookInfoList})

@app.route("/backend/getCommentInfo")
@cross_origin(origin='localhost',headers=['Content- Type'])
def getCommentInfo():
    bookId = request.args.get("bookId")
    cur.execute("SELECT c.comment_id, a.account_name, c.comment_description from comments c join account a on c.account_id = a.account_id where c.book_id=%s", (bookId))
    rows = cur.fetchall()
    print(rows)
    commentsList = []
    for i in range(len(rows)):
        commentInfo = {
            "id": rows[i][0],
            "user": rows[i][1],
            "description": rows[i][2]
        }
        commentsList.append(commentInfo)
    
    return jsonify({"comments": commentsList})

@app.route("/backend/sendComment", methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type'])
def sendComment():
    commentData = request.get_json()

    cur.execute("INSERT into comments values((SELECT MAX( comment_id )+1 FROM comments), %s, %s, %s)", (commentData["description"], commentData["userId"], commentData["bookId"]))
    # rows = cur.fetchall()
    connection.commit()

    return jsonify({"addComment": True})


@app.route("/backend/sendOrder", methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type'])
def sendOrder():
    orderData = request.get_json()
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
@cross_origin(origin='localhost',headers=['Content- Type'])
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
@cross_origin(origin='localhost',headers=['Content- Type'])
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
@cross_origin(orgin='localhost', headers=['Content-Type'])
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
@cross_origin(orgin='localhost', headers=['Content-Type'])
def getAllComment():
    cur.execute("SELECT * from order_comment")
    rows = cur.fetchall()
    print(rows)
    commentsList = []
    for i in range(len(rows)):
        commentInfo = {
            "id": rows[i][0],
            "description": rows[i][1]
        }
        commentsList.append(commentInfo)
    
    return jsonify({"comments": commentsList})

@app.route("/backend/sendCommentFOrOrder", methods=['POST'])
@cross_origin(orgin='localhost', headers=['Content-Type'])
def sendCommentFOrOrder():

    commentData = request.get_json()

    cur.execute("INSERT into order_comment values((SELECT MAX( comment_id )+1 FROM order_comment), %s)", [commentData["description"]])
    # rows = cur.fetchall()
    connection.commit()

    return jsonify({"addComment": True})

@app.route("/backend/removeComment", methods=['POST'])
@cross_origin(orgin='localhost', headers=['Content-Type'])
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

if __name__ == "__main__":
    app.debug = True
    app.run(host= databaseIP)
