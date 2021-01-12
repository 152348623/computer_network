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
cors = CORS(app, resources={r"/backend/": {"origins": "https://" + databaseIP + ":5000"}})
app.config['DEBUG'] = True
connection = psycopg2.connect(database="networkcomputer",
                              user="admin", password="sunbird", host=databaseIP, port="5432")
cur = connection.cursor()

@app.route('/')
def run():
    return 'My Flask App!'


@app.route("/backend/sendOrder", methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type'])
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
    app.run(host= databaseIP, ssl_context ='adhoc' )
