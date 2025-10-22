import tkinter as tk
import functions as f

"""--- Variáveis globais ---"""

cbValues = {}
cbIds = []

"""--- Funções principais ---"""

def clearAll():
  for w in main.winfo_children():
    w.destroy()

def showMenu():
  clearAll()

  aux = tk.Frame(main)
  aux.pack(fill="both", expand=True)
  
  style = {"width": 16, "height": 2}
  tk.Button(aux, **style, text="Adicionar", font=("consolas", 12, "normal"), command=lambda:showAdd()).pack(pady=16)
  tk.Button(aux, **style, text="Remover", font=("consolas", 12, "normal"), command=lambda:showRemove()).pack(pady=16)
  tk.Button(aux, **style, text="Apagar Tudo", font=("consolas", 12, "normal"), command=lambda:print("0")).pack(pady=16)
  tk.Button(aux, **style, text="Ver Senhas", font=("consolas", 12, "normal"), command=lambda:print("0")).pack(pady=16)

"""--- Funções de auxiliares ---"""

def changeState(id, var):
  if var.get() == True:
    cbIds.append(id)
    print(f"Checkbox {id} marcado")
  else:
    cbIds.remove(id)
    print(f"Checkbox {id} desmarcado")

def iterateIds():
  for id in cbIds:
    f.removePassword(id)
  
  showMenu()

"""--- Funções de frontend ---"""

def showAdd():
  clearAll()

  aux = tk.Frame(main)
  aux.pack(fill="both", expand=True)

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

  salvar = tk.Button(btnFrame, width=8, height=2, text="Salvar", command=lambda:f.addPassword(tipo.get(), email.get(), telefone.get(), user.get(), senha.get()))
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
    cbValues[idRegistro] = varState
    
    tk.Checkbutton(fList, variable=varState, command=lambda id=idRegistro, var=varState: changeState(id, var)).grid(row=rowNum, column=0, sticky="w", padx=16, pady=4)
    
    tk.Label(fList, text=f"{row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}", font=("consolas", 12, "normal")).grid(row=rowNum, column=1, sticky="e", padx=16, pady=4)
    
    rowNum += 1
  
  del rowNum
  
  deletar = tk.Button(fButton, width=8, height=2, text="Remover", command=lambda:iterateIds())
  deletar.pack(side="left", padx=16)
  voltar = tk.Button(fButton, width=8, height=2, text="Voltar", command=lambda:showMenu())
  voltar.pack(side="right", padx=16)

"""--- Main ---"""

root = tk.Tk()
root.title("Gerenciador de Senhas")
root.geometry("750x500")
root.resizable(False, False)

main = tk.Frame(root)
main.pack(fill="both", expand=True)

showMenu()

root.mainloop()