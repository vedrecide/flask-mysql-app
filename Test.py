import json
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from uuid import uuid4


with open("./config.json", "r") as f:
  config = json.loads(f.read())


try:
  
  conn = connection.MySQLConnection(
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

cur.execute(f"DESC Question")

for row in cur.fetchall():
  print(' | '.join(str(elem) for elem in row))


