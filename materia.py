import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

# Função para carregar as matérias na Combobox
def carregar_materias():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxxxxx'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            # Consultar todas as matérias
            query = "SELECT nome FROM materia"
            cursor.execute(query)
            materias = cursor.fetchall()
            
            # Limpar e atualizar a Combobox com as matérias
            combobox_materias['values'] = [materia[0] for materia in materias]
            combobox_materias.set('')  # Limpa a seleção atual

    except Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar matérias: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para cadastrar uma nova matéria
def cadastrar_materia():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxxxx'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            # Verificar se a matéria já existe
            query_verificar = "SELECT nome FROM materia WHERE nome = %s"
            cursor.execute(query_verificar, (entry_nome_materia.get(),))
            resultado = cursor.fetchone()
            
            if resultado:
                messagebox.showwarning("Aviso", "Matéria já cadastrada!")
            else:
                # Inserir nova matéria
                query_inserir = "INSERT INTO materia (nome) VALUES (%s)"
                valores = (entry_nome_materia.get(),)
                
                cursor.execute(query_inserir, valores)
                conexao.commit()

                messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
                entry_nome_materia.delete(0, tk.END)
                carregar_materias()  # Atualiza a Combobox após o cadastro

    except Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar matéria: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para excluir a matéria selecionada
def excluir_materia():
    materia_selecionada = combobox_materias.get()
    if not materia_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma matéria para excluir.")
        return

    resposta = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir a matéria '{materia_selecionada}'?")
    if resposta:
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                database='teste',
                user='root',
                password='xxxxxxxxxx'
            )

            if conexao.is_connected():
                cursor = conexao.cursor()
                # Excluir a matéria
                query_excluir = "DELETE FROM materia WHERE nome = %s"
                cursor.execute(query_excluir, (materia_selecionada,))
                conexao.commit()

                messagebox.showinfo("Sucesso", f"Matéria '{materia_selecionada}' excluída com sucesso!")
                carregar_materias()  # Atualiza a Combobox após exclusão

        except Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir matéria: {e}")
        
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Criar a janela principal
janela = tk.Tk()
janela.title("Cadastro e Exclusão de Matéria")

# Caixa de texto para nome da matéria
label_nome_materia = tk.Label(janela, text="Nome da Matéria:")
label_nome_materia.grid(row=0, column=0)
entry_nome_materia = tk.Entry(janela)
entry_nome_materia.grid(row=0, column=1)

# Botão de cadastrar
botao_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_materia)
botao_cadastrar.grid(row=1, column=1)

# Combobox para selecionar matéria cadastrada
label_materias = tk.Label(janela, text="Selecionar Matéria para Exclusão:")
label_materias.grid(row=2, column=0)
combobox_materias = ttk.Combobox(janela, width=28)
combobox_materias.grid(row=2, column=1)

# Botão de excluir
botao_excluir = tk.Button(janela, text="Excluir", command=excluir_materia)
botao_excluir.grid(row=3, column=1)

# Carregar as matérias na inicialização
carregar_materias()

# Executar o loop da interface gráfica
janela.mainloop()
