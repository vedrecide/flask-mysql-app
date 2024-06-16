from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt

import json
import mysql.connector
from mysql.connector import errorcode
from uuid import uuid4


with open("./config.json", "r") as f:
  config = json.loads(f.read())

app = Flask(__name__)
bcrypt = Bcrypt(app)
try:
  conn = mysql.connector.connect(
    user=config["DATABASE_USER"], 
    password=config["DATABASE_PASSWORD"], 
    host=config["DATABASE_HOST"], 
    port=config["DATABASE_PORT"], 
    database=config["DATABASE_NAME"]
  )
  cur = conn.cursor()
  print("Connection established successfully", flush=True)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password", flush=True)
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist", flush=True)
  else:
    print(err, flush=True)

with app.app_context():
  cur.execute("CREATE TABLE IF NOT EXISTS User(id CHAR(36) PRIMARY KEY, username VARCHAR(30) NOT NULL, password VARCHAR(60) NOT NULL, teacher TINYINT)")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/questions")
def questions():
  return render_template("questions.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  error = None
  success = None
  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')
    is_teacher = 1 if request.form.get("teacher") is not None else 0

    if len(username) < 8 or len(password) < 8:
      error = "Username or password cannot be less than 8 characters, Choose wisely young/old one"
    else:
      cur.execute(f"SELECT * FROM User WHERE username = '{username}'")
      user = cur.fetchone()
      if user is not None:
        error = "User already exists, Are you a clone trooper?"
      else:
        hashpw = bcrypt.generate_password_hash(password)
        real_password = hashpw.decode("ascii")
        print(real_password, flush=True)
        cur.execute("INSERT INTO User (id, username, password, teacher) VALUES(%s, %s, %s, %s)", (str(uuid4()), username, real_password, is_teacher))
        conn.commit()

        cur.execute(f"SELECT * FROM User WHERE username = '{username}'")
        user = cur.fetchone()
        print(user, flush=True)
        
        success = "Successfully authorized into the Jedi temple"

        # print(username, password, is_teacher, flush=True)
  return render_template("login.html", error=error, success=success)

if __name__ == "__main__":
  app.run(debug=bool(config["DEBUG"]))
