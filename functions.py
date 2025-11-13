import mysql.connector

config = {
  "host": "localhost",
  "user": "root",
  "password": "",
  "database": ".password_manager"
}

def connect():
  return mysql.connector.connect(**config)

def addPassword(tipo: str, email: str, telefone: str, user: str, password: str):
  con = connect()
  cur = con.cursor()
  cur.execute("INSERT INTO senhas (tipo, email, telefone, user, password) VALUES (%s, %s, %s, %s, %s)", (tipo, email, telefone, user, password))
  con.commit()
  cur.close()
  con.close()