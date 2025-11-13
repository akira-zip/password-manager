import tkinter as tk
import functions as f
import variables as v

"""
--- Funções principais ---
"""

def clearAll():
  for w in main.winfo_children():
    w.destroy()

def showMenu():
  clearAll()

  aux = tk.Frame(main)
  aux.pack(fill="both", expand=True)
  
  style = {"width": 16, "height": 2}
  tk.Button(aux, **style, text="Adicionar", font=("consolas", 12, "normal"), command=lambda:showAdd()).pack(pady=16)
  tk.Button(aux, **style, text="Ver Senhas", font=("consolas", 12, "normal"), command=lambda:showSelect()).pack(pady=16)
  tk.Button(aux, **style, text="Remover", font=("consolas", 12, "normal"), command=lambda:showRemove()).pack(pady=16)
  tk.Button(aux, **style, text="Apagar Tudo", font=("consolas", 12, "normal"), command=lambda:f.removeAllPasswords()).pack(pady=16)

"""
--- Funções de auxiliares ---
"""

def save(tipo, email, telefone, user, senha):
  f.addPassword(tipo, email, telefone, user, senha)
  showMenu()

def changeState(id, var):
  if var.get() == True:
    v.cbIds.append(id)
    print(f"Checkbox {id} marcado")
  else:
    v.cbIds.remove(id)
    print(f"Checkbox {id} desmarcado")

def iterateIds():
  for id in v.cbIds:
    f.removePassword(id)
  
  showMenu()

"""
--- Funções de frontend ---
"""

def showAdd():
  clearAll()

  aux = tk.Frame(main)
  aux.pack()

  title = tk.Label(aux, text="Adicionar senha", font=("consolas", 16, "bold"))
  title.grid(row=0, column=0, sticky="ew", pady=16)
  
  tk.Label(aux, text="Tipo (site)", font=("consolas", 12, "normal")).grid(row=1, column=0, sticky="w", pady=2)
  tipo = tk.Entry(aux, width=40)
  tipo.grid(row=2, column=0, sticky="w", pady=4)

  tk.Label(aux, text="Email", font=("consolas", 12, "normal")).grid(row=3, column=0, sticky="w", pady=2)
  email = tk.Entry(aux, width=40)
  email.grid(row=4, column=0, sticky="w", pady=4)

  tk.Label(aux, text="Telefone", font=("consolas", 12, "normal")).grid(row=5, column=0, sticky="w", pady=2)
  telefone = tk.Entry(aux, width=40)
  telefone.grid(row=6, column=0, sticky="w", pady=4)

  tk.Label(aux, text="Usuário", font=("consolas", 12, "normal")).grid(row=7, column=0, sticky="w", pady=2)
  user = tk.Entry(aux, width=40)
  user.grid(row=8, column=0, sticky="w", pady=4)

  tk.Label(aux, text="Senha", font=("consolas", 12, "normal")).grid(row=9, column=0, sticky="w", pady=2)
  senha = tk.Entry(aux, width=40)
  senha.grid(row=10, column=0, sticky="w", pady=4)

  btnFrame = tk.Frame(aux)
  btnFrame.grid(row=11, column=0, sticky="ew")

  salvar = tk.Button(btnFrame, width=8, height=2, text="Salvar", command=lambda:save(tipo.get(), email.get(), telefone.get(), user.get(), senha.get()))
  salvar.pack(side="left", pady=16)

  voltar = tk.Button(btnFrame, width=8, height=2, text="Voltar", command=lambda:showMenu())
  voltar.pack(side="right", pady=16)

def showRemove():
  clearAll()

  aux = tk.Frame(main)
  aux.pack(fill="both")

  title = tk.Label(aux, text="Remover senhas", font=("consolas", 16, "bold"))
  title.pack(side="top", pady=16)

  fList = tk.Frame(aux)
  fList.pack(fill="both", expand=True, pady=16)
  fButton = tk.Frame(aux)
  fButton.pack(pady=16)
  
  rowNum = 1
  
  for row in f.loadPasswords():
    idRegistro = row[0]
    varState = tk.BooleanVar()
    v.cbValues[idRegistro] = varState
    
    tk.Checkbutton(fList, variable=varState, command=lambda id=idRegistro, var=varState: changeState(id, var)).grid(row=rowNum, column=0, sticky="w", padx=16, pady=4)
    
    tk.Label(fList, text=f"{row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}", font=("consolas", 12, "normal")).grid(row=rowNum, column=1, sticky="e", padx=16, pady=4)
    
    rowNum += 1
  
  del rowNum
  
  deletar = tk.Button(fButton, width=8, height=2, text="Remover", command=lambda:iterateIds())
  deletar.pack(side="left", padx=16)
  voltar = tk.Button(fButton, width=8, height=2, text="Voltar", command=lambda:showMenu())
  voltar.pack(side="right", padx=16)

def showSelect():
  clearAll()

  aux = tk.Frame(main)
  aux.pack()

  title = tk.Label(aux, text="Adicionar senha", font=("consolas", 16, "bold"))
  title.pack(fill="x", pady=16)

  selectList = tk.Frame(aux)
  selectList.pack(fill="both", expand=True, pady=16)

  tk.Label(selectList, text="Id", font=("consolas", 12, "bold")).grid(row=0, column=0, sticky="ew", padx=16)
  tk.Label(selectList, text="Tipo", font=("consolas", 12, "bold")).grid(row=0, column=1, sticky="ew", padx=16)
  tk.Label(selectList, text="Email", font=("consolas", 12, "bold")).grid(row=0, column=2, sticky="ew", padx=16)
  tk.Label(selectList, text="Telefone", font=("consolas", 12, "bold")).grid(row=0, column=3, sticky="ew", padx=16)
  tk.Label(selectList, text="Usuário", font=("consolas", 12, "bold")).grid(row=0, column=4, sticky="ew", padx=16)
  tk.Label(selectList, text="Senha", font=("consolas", 12, "bold")).grid(row=0, column=5, sticky="ew", padx=16)
  cont = 1

  for row in f.loadPasswords():
    tk.Label(selectList, text=row[0], font=("consolas", 12, "normal")).grid(row=cont, column=0, sticky="ew")
    tk.Label(selectList, text=row[1], font=("consolas", 12, "normal")).grid(row=cont, column=1, sticky="ew")
    tk.Label(selectList, text=row[2], font=("consolas", 12, "normal")).grid(row=cont, column=2, sticky="ew")
    tk.Label(selectList, text=row[3], font=("consolas", 12, "normal")).grid(row=cont, column=3, sticky="ew")
    tk.Label(selectList, text=row[4], font=("consolas", 12, "normal")).grid(row=cont, column=4, sticky="ew")
    tk.Label(selectList, text=row[5], font=("consolas", 12, "normal")).grid(row=cont, column=5, sticky="ew")
    cont += 1

  btnFrame = tk.Frame(aux)
  btnFrame.pack(fill="x", pady=16)

  voltar = tk.Button(btnFrame, width=8, height=2, text="Voltar", command=lambda:showMenu())
  voltar.pack(side="right", pady=16)

"""
--- Main ---
"""

root = tk.Tk()
root.title("Gerenciador de Senhas")
root.geometry("750x500")
root.resizable(False, False)

main = tk.Frame(root)
main.pack(fill="both", expand=True)

showMenu()

root.mainloop()