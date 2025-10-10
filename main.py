import tkinter as tk
import mysql.connector

import _mysql_connector

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

def removePassword(id: int):
  con = connect()
  cur = con.cursor()
  cur.execute("DELETE FROM senhas WHERE id = %d", (id))
  con.commit()
  cur.close()
  con.close()

def removeAllPasswords():
  con = connect()
  cur = con.cursor()
  cur.execute("DELETE FROM senhas")
  con.commit()
  con.close()

def loadPasswords():
  con = connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM senhas")
  resultados = cur.fetchall()

  for resultado in resultados:
    print(resultado)

  cur.close()
  con.close()