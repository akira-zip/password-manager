import tkinter as tk
from tkinter import messagebox
import os

# --- Configurações de Armazenamento ---
# Aviso de segurança: Em uma aplicação real, use criptografia e/ou um banco de dados seguro!
PASSWORD_FILE = "passwords.txt"

def load_passwords():
    """Carrega as senhas do arquivo de texto, tratando a estrutura de dados."""
    passwords = []
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            for line in file:
                # O formato esperado é: Tipo|Email|Telefone|Usuario|Senha
                parts = line.strip().split('|')
                if len(parts) == 5:
                    passwords.append({
                        "Tipo": parts[0],
                        "Email": parts[1],
                        "Telefone": parts[2],
                        "Usuario": parts[3],
                        "Senha": parts[4]
                    })
    return passwords

def save_passwords(passwords):
    """Salva a lista atualizada de senhas no arquivo de texto."""
    with open(PASSWORD_FILE, 'w') as file:
        for p in passwords:
            line = f"{p['Tipo']}|{p['Email']}|{p['Telefone']}|{p['Usuario']}|{p['Senha']}\n"
            file.write(line)

# --- Classe Principal da Aplicação ---

class PasswordManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Senhas")
        master.geometry("400x250") # Tamanho inicial razoável

        # Variável para rastrear a tela atual e poder limpá-la
        self.current_frame = None

        # Configura a tela principal com os botões de navegação
        self.setup_main_menu()

    def clear_frame(self):
        """Limpa a tela atual para carregar uma nova."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.master, padx=10, pady=10)
        self.current_frame.pack(fill='both', expand=True)
        return self.current_frame

    # --- Tela do Menu Principal ---
    def setup_main_menu(self):
        """Cria os botões da tela inicial conforme o PDF."""
        main_frame = self.clear_frame()
        
        tk.Label(main_frame, text="Menu Principal", font=("Arial", 16, "bold")).pack(pady=10)

        # Botão: Adicionar senhas
        tk.Button(main_frame, text="Adicionar Senhas", command=self.add_password_screen, width=30).pack(pady=5)
        # Botão: Excluir senhas
        tk.Button(main_frame, text="Excluir Senhas", command=self.delete_password_screen, width=30).pack(pady=5)
        # Botão: Olhar senhas
        tk.Button(main_frame, text="Olhar Senhas", command=self.view_passwords_screen, width=30).pack(pady=5)
        # Botão: Resetar senhas
        tk.Button(main_frame, text="Resetar Senhas (Apagar Tudo)", command=self.reset_passwords, width=30, fg='red').pack(pady=5)

    # --- Funcionalidade: Adicionar Senhas ---
    def add_password_screen(self):
        """Cria a tela para adicionar novas senhas."""
        add_frame = self.clear_frame()
        self.master.title("Adicionar Senha")

        tk.Label(add_frame, text="Adicionar Nova Senha", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos de entrada
        fields = ["Tipo", "Email", "Número de Telefone", "Usuário", "Password"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(add_frame, text=f"{field}:").grid(row=i+1, column=0, padx=5, pady=2, sticky='e')
            entry = tk.Entry(add_frame, width=30)
            
            # Esconder a senha digitada
            if field == "Password":
                entry.config(show='*')
            
            entry.grid(row=i+1, column=1, padx=5, pady=2, sticky='w')
            self.entries[field] = entry

        # Botão para adicionar as informações
        tk.Button(add_frame, text="Adicionar", command=self.save_new_password, width=15).grid(row=len(fields)+1, column=1, pady=10, sticky='w')
        # Botão para voltar
        tk.Button(add_frame, text="Voltar ao Menu", command=self.setup_main_menu).grid(row=len(fields)+1, column=0, pady=10, sticky='e')

    def save_new_password(self):
        """Coleta e salva os dados da nova senha."""
        new_data = {key: entry.get() for key, entry in self.entries.items()}
        
        # Validação básica
        if any(not value for value in new_data.values()):
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos!")
            return

        passwords = load_passwords()
        passwords.append(new_data)
        save_passwords(passwords)

        messagebox.showinfo("Sucesso", "Senha adicionada com sucesso!")
        
        # Limpa os campos após salvar
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # --- Funcionalidade: Olhar Senhas ---
    def view_passwords_screen(self):
        """Cria a tela para o usuário observar todas as senhas anotadas."""
        view_frame = self.clear_frame()
        self.master.title("Olhar Senhas")
        self.master.geometry("800x400") # Aumenta o tamanho para a visualização

        tk.Label(view_frame, text="Senhas Cadastradas", font=("Arial", 14)).pack(pady=10)

        passwords = load_passwords()

        if not passwords:
            tk.Label(view_frame, text="Nenhuma senha cadastrada.").pack(pady=20)
        else:
            # Estrutura para exibir a tabela de senhas
            
            # Cabeçalhos
            headers = ["Tipo", "Email", "Telefone", "Usuário", "Senha"]
            for col, header in enumerate(headers):
                tk.Label(view_frame, text=header, font=("Arial", 10, "bold"), relief="raised", padx=5, pady=5).grid(row=1, column=col, sticky="nsew")

            # Dados
            for row, p in enumerate(passwords):
                for col, key in enumerate(headers):
                    value = p.get(key, 'N/A')
                    tk.Label(view_frame, text=value, relief="groove", padx=5, pady=5).grid(row=row+2, column=col, sticky="nsew")

        tk.Button(view_frame, text="Voltar ao Menu", command=self.setup_main_menu).pack(pady=20)

    # --- Funcionalidade: Excluir Senhas ---
    def delete_password_screen(self):
        """Cria a tela para visualizar senhas com checkbox e excluir."""
        delete_frame = self.clear_frame()
        self.master.title("Excluir Senhas")
        self.master.geometry("800x400")

        tk.Label(delete_frame, text="Excluir Senhas", font=("Arial", 14)).pack(pady=10)

        passwords = load_passwords()
        self.delete_vars = [] # Variável para armazenar os Checkbuttons (para saber quais excluir)

        if not passwords:
            tk.Label(delete_frame, text="Nenhuma senha cadastrada para excluir.").pack(pady=20)
        else:
            # Tabela com Checkboxes
            
            # Cabeçalhos
            headers = ["Excluir", "Tipo", "Email", "Usuário"] # Simplifiquei a visualização para exclusão
            for col, header in enumerate(headers):
                tk.Label(delete_frame, text=header, font=("Arial", 10, "bold"), relief="raised", padx=5, pady=5).grid(row=1, column=col, sticky="nsew")

            # Dados com Checkbox
            for row, p in enumerate(passwords):
                var = tk.BooleanVar()
                self.delete_vars.append(var)
                
                # Checkbox
                tk.Checkbutton(delete_frame, variable=var).grid(row=row+2, column=0, padx=5, pady=2, sticky='n')
                
                # Dados
                tk.Label(delete_frame, text=p.get("Tipo", 'N/A'), relief="groove", padx=5, pady=5).grid(row=row+2, column=1, sticky="nsew")
                tk.Label(delete_frame, text=p.get("Email", 'N/A'), relief="groove", padx=5, pady=5).grid(row=row+2, column=2, sticky="nsew")
                tk.Label(delete_frame, text=p.get("Usuario", 'N/A'), relief="groove", padx=5, pady=5).grid(row=row+2, column=3, sticky="nsew")
                

            # Botão para excluir
            tk.Button(delete_frame, text="Excluir Senhas Selecionadas", command=lambda: self.perform_delete(passwords), fg='red').pack(pady=10)
        
        tk.Button(delete_frame, text="Voltar ao Menu", command=self.setup_main_menu).pack(pady=5)


    def perform_delete(self, old_passwords):
        """Executa a exclusão das senhas marcadas e salva o restante."""
        if not self.delete_vars:
            messagebox.showinfo("Aviso", "Nenhuma senha para excluir.")
            return

        # Cria uma nova lista apenas com as senhas NÃO marcadas
        new_passwords = []
        deleted_count = 0
        for i, p in enumerate(old_passwords):
            if not self.delete_vars[i].get(): # Se o checkbox NÃO estiver marcado
                new_passwords.append(p)
            else:
                deleted_count += 1

        if deleted_count == 0:
            messagebox.showinfo("Aviso", "Nenhuma senha foi selecionada para exclusão.")
            return

        # Confirmação antes de excluir
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir {deleted_count} senha(s) selecionada(s)?"):
            save_passwords(new_passwords)
            messagebox.showinfo("Sucesso", f"{deleted_count} senha(s) excluída(s) com sucesso!")
            # Recarrega a tela de exclusão para mostrar o resultado
            self.delete_password_screen()
        
    # --- Funcionalidade: Resetar Senhas ---
    def reset_passwords(self):
        """Apaga todas as senhas."""
        if messagebox.askyesno("CONFIRMAÇÃO CRÍTICA", "ATENÇÃO! Você tem certeza que deseja APAGAR TODAS AS SENHAS? Esta ação é irreversível."):
            try:
                if os.path.exists(PASSWORD_FILE):
                    os.remove(PASSWORD_FILE)
                messagebox.showinfo("Sucesso", "Todas as senhas foram apagadas.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao apagar as senhas: {e}")
            finally:
                self.setup_main_menu() # Volta para o menu principal

# --- Execução do Programa ---

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()