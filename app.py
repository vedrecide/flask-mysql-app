from flask import Flask, render_template
from flask_bcrypt import Bcrypt

import json
import mysql.connector
from mysql.connector import errorcode
from uuid import uuid4


with open("./config.json", "r") as f:
  config = json.loads(f.read())

app = Flask(__name__)
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
  cur.execute("CREATE TABLE IF NOT EXISTS User(id CHAR(36) PRIMARY KEY, username VARCHAR(30) NOT NULL, password BINARY(60) NOT NULL, teacher TINYINT)")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/questions")
def questions():
  return render_template("questions.html")

if __name__ == "__main__":
  app.run(debug=bool(config["DEBUG"]))
