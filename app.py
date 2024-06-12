from flask import Flask

import json
import mysql.connector
from mysql.connector import errorcode


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
  print("Connection established successfully", flush=True)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password", flush=True)
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist", flush=True)
  else:
    print(err, flush=True)
else:
  conn.close()


@app.route("/")
def home():
  return "Home"

if __name__ == "__main__":
  app.run(debug=bool(config["DEBUG"]))
