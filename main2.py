import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- UI helpers ----------------
def clear_main():
    # remove tudo que está no container principal
    for w in main_container.winfo_children():
        w.destroy()

def show_main_menu():
    clear_main()
    frm = tk.Frame(main_container)
    frm.pack(expand=True)

    # colocar os botões centralizados em coluna
    btn_style = {"width": 20, "height": 2, "padx": 8, "pady": 8}
    tk.Button(frm, text="Adicionar", command=show_add_screen, **btn_style).pack(pady=6)
    tk.Button(frm, text="Remover", command=show_remove_screen, **btn_style).pack(pady=6)
    tk.Button(frm, text="Apagar Tudo", command=action_delete_all_confirm, **btn_style).pack(pady=6)
    tk.Button(frm, text="Ver Senhas", command=show_view_screen, **btn_style).pack(pady=6)

def show_add_screen():
    clear_main()
    frm = tk.Frame(main_container, padx=12, pady=12)
    frm.pack(fill=tk.BOTH, expand=True)

    title = tk.Label(frm, text="Adicionar senha", font=("TkDefaultFont", 14, "bold"))
    title.grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")

    tk.Label(frm, text="Tipo (site):").grid(row=1, column=0, sticky="e", pady=4)
    entry_tipo = tk.Entry(frm, width=40)
    entry_tipo.grid(row=1, column=1, sticky="w", pady=4)

    tk.Label(frm, text="Email:").grid(row=2, column=0, sticky="e", pady=4)
    entry_email = tk.Entry(frm, width=40)
    entry_email.grid(row=2, column=1, sticky="w", pady=4)

    tk.Label(frm, text="Telefone:").grid(row=3, column=0, sticky="e", pady=4)
    entry_telefone = tk.Entry(frm, width=40)
    entry_telefone.grid(row=3, column=1, sticky="w", pady=4)

    tk.Label(frm, text="User:").grid(row=4, column=0, sticky="e", pady=4)
    entry_user = tk.Entry(frm, width=40)
    entry_user.grid(row=4, column=1, sticky="w", pady=4)

    tk.Label(frm, text="Password:").grid(row=5, column=0, sticky="e", pady=4)
    entry_password = tk.Entry(frm, width=40, show="*")
    entry_password.grid(row=5, column=1, sticky="w", pady=4)

    # botão mostrar/esconder no campo de senha
    def toggle_show():
        if entry_password.cget("show") == "":
            entry_password.config(show="*")
            btn_toggle.config(text="Mostrar")
        else:
            entry_password.config(show="")
            btn_toggle.config(text="Esconder")

    btn_toggle = tk.Button(frm, text="Mostrar", command=toggle_show)
    btn_toggle.grid(row=5, column=2, padx=(10,0))

    # ações: salvar e voltar
    def action_save():
        tipo = entry_tipo.get().strip()
        email = entry_email.get().strip()
        telefone = entry_telefone.get().strip()
        usuario = entry_user.get().strip()
        password = entry_password.get().strip()
        if not tipo or not password:
            messagebox.showwarning("Atenção", "Preencha ao menos 'Tipo' e 'Password'.")
            return
        try:
            add_password_db(tipo, email, telefone, usuario, password)
            messagebox.showinfo("Salvo", "Senha salva com sucesso.")
            # limpar campos depois de salvar
            entry_tipo.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_password.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar:\n{e}")

    btn_frame = tk.Frame(frm, pady=12)
    btn_frame.grid(row=6, column=0, columnspan=3)

    tk.Button(btn_frame, text="Salvar", width=12, command=action_save).pack(side=tk.LEFT, padx=6)
    tk.Button(btn_frame, text="Voltar", width=12, command=show_main_menu).pack(side=tk.LEFT, padx=6)

def show_remove_screen():
    clear_main()
    frm = tk.Frame(main_container, padx=8, pady=8)
    frm.pack(fill=tk.BOTH, expand=True)

    title = tk.Label(frm, text="Remover senhas", font=("TkDefaultFont", 14, "bold"))
    title.pack(anchor="w")

    # área com scroll para listar cada senha com checkbox à esquerda
    list_frame = tk.Frame(frm)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=(8,6))

    canvas = tk.Canvas(list_frame)
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas)

    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # carregar senhas e criar checkbuttons
    rows = get_all_passwords()
    remove_vars.clear()  # map id -> BooleanVar
    if not rows:
        tk.Label(inner, text="Nenhuma senha encontrada.", pady=8).pack()
    else:
        # cabeçalho simples
        hdr = tk.Frame(inner)
        hdr.pack(fill=tk.X, pady=(0,6))
        tk.Label(hdr, text="", width=3).grid(row=0, column=0)  # espaço do checkbox
        tk.Label(hdr, text="Tipo", width=25, anchor="w", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(hdr, text="User", width=20, anchor="w", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, sticky="w")
        tk.Label(hdr, text="Email", width=25, anchor="w", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, sticky="w")
        tk.Label(hdr, text="Telefone", width=15, anchor="w", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=4, sticky="w")

        for r in rows:
            rid, tipo, email, telefone, usuario, password = r
            vf = tk.BooleanVar(value=False)
            remove_vars[rid] = vf
            rowf = tk.Frame(inner)
            rowf.pack(fill=tk.X, pady=2)
            cb = tk.Checkbutton(rowf, variable=vf)
            cb.grid(row=0, column=0, padx=(0,6))
            tk.Label(rowf, text=tipo, width=25, anchor="w").grid(row=0, column=1, sticky="w")
            tk.Label(rowf, text=usuario or "-", width=20, anchor="w").grid(row=0, column=2, sticky="w")
            tk.Label(rowf, text=email or "-", width=25, anchor="w").grid(row=0, column=3, sticky="w")
            tk.Label(rowf, text=telefone or "-", width=15, anchor="w").grid(row=0, column=4, sticky="w")

    # botões remover e voltar
    btns = tk.Frame(frm, pady=10)
    btns.pack(fill=tk.X)
    def action_remove_selected():
        selected_ids = [rid for rid, var in remove_vars.items() if var.get()]
        if not selected_ids:
            messagebox.showinfo("Info", "Marque pelo menos uma senha para remover.")
            return
        if not messagebox.askyesno("Confirmar", f"Remover {len(selected_ids)} item(s)?"):
            return
        try:
            delete_passwords_by_ids(selected_ids)
            messagebox.showinfo("Removido", "Itens removidos com sucesso.")
            show_remove_screen()  # recarregar a tela
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao remover:\n{e}")

    tk.Button(btns, text="Remover", width=12, command=action_remove_selected).pack(side=tk.LEFT, padx=6)
    tk.Button(btns, text="Voltar", width=12, command=show_main_menu).pack(side=tk.LEFT, padx=6)

def show_view_screen():
    clear_main()
    frm = tk.Frame(main_container, padx=8, pady=8)
    frm.pack(fill=tk.BOTH, expand=True)

    title = tk.Label(frm, text="Todas as senhas", font=("TkDefaultFont", 14, "bold"))
    title.pack(anchor="w")

    cols = ("id","tipo","email","telefone","usuario","password")
    tree = ttk.Treeview(frm, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.capitalize())
        if c == "tipo":
            tree.column(c, width=180, anchor="w")
        elif c == "password":
            tree.column(c, width=160, anchor="w")
        else:
            tree.column(c, width=120, anchor="w")

    vsb = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    # carregar dados
    rows = get_all_passwords()
    for r in rows:
        tree.insert("", tk.END, values=r)

    # botão voltar embaixo
    btn_frame = tk.Frame(frm, pady=8)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Voltar", width=12, command=show_main_menu).pack(side=tk.LEFT, padx=6)

# ---------------- actions ----------------
def action_delete_all_confirm():
    if not messagebox.askyesno("Confirmar", "Apagar todas as senhas do banco? Esta ação é irreversível."):
        return
    try:
        messagebox.showinfo("Apagado", "Todas as senhas foram apagadas.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao apagar:\n{e}")

# ---------------- main ----------------

root = tk.Tk()
root.title("Gerenciador de Senhas - Simples")
root.geometry("840x560")
root.minsize(640, 420)

main_container = tk.Frame(root)
main_container.pack(fill=tk.BOTH)

# mapa global para variáveis dos checkboxes na tela de remover
remove_vars = dict()

show_main_menu()

root.mainloop()