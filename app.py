from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)
port = 5000

connection = mysql.connector.connect(
    host='localhost',
    database='instabook',
    user='instabook_admin',
    password='admin',
)


@app.get('/')
def say_hello():
    return "Hello world"


@app.get('/books')
def get_books():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT b.id, b.title, b.author, ROUND(AVG(r.score), 1) AS rating
                      FROM books AS b
                      JOIN book_ratings AS r
                      ON b.id = r.book_id
                      GROUP BY b.id;""")
    results = cursor.fetchall()
    cursor.close()
    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.get('/books/<int:book_id>')
def get_book_by_id(book_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT b.id, b.title, b.author, ROUND(AVG(r.score), 1) AS rating
                      FROM books AS b
                      JOIN book_ratings AS r
                      ON b.id = r.book_id
                      WHERE b.id = %s
                      GROUP BY b.id""", [book_id])
    result = cursor.fetchone()
    cursor.close()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.get('/users')
def get_users():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT u.id, u.username, u.display_name
                      FROM users u""")
    results = cursor.fetchall()
    cursor.close()
    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.get('/users/<int:user_id>')
def get_user_by_id(user_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""SELECT u.id, u.username, u.display_name
                      FROM users AS u
                      WHERE u.id = %s""", [user_id])
    result = cursor.fetchone()
    cursor.close()
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.run(port=port)
