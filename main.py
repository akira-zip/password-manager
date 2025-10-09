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

def loadPasswords():
  con = connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM senhas")
  resultados = cur.fetchall()

  for [id, tipo, email, telefone, user, password] in resultados:
    print(f"[Id] {id} | [Tipo] {tipo} | [Email] {email} | [Telefone] {telefone} | [Usuario] {user} | [Senha] {password}")

  cur.close()
  con.close()