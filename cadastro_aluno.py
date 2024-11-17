import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Função para validar e formatar a data
def formatar_data(data_texto):
    try:
        data_formatada = datetime.strptime(data_texto, '%d/%m/%Y').strftime('%Y-%m-%d')
        return data_formatada
    except ValueError:
        messagebox.showerror("Erro", f"Formato de data inválido: {data_texto}. Use o formato DD/MM/YYYY.")
        return None

# Função para verificar duplicidade de ID ou CPF
def verificar_duplicidade(conexao, id_aluno, cpf):
    cursor = conexao.cursor()
    query = "SELECT id FROM cadastro_de_aluno WHERE id = %s OR cpf = %s"
    cursor.execute(query, (id_aluno, cpf))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None

# Função para inserir dados no banco de dados
def cadastrar_aluno():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxx'
        )
        
        if conexao.is_connected():
            # Verificar duplicidade
            if verificar_duplicidade(conexao, entry_id.get(), entry_cpf.get()):
                messagebox.showerror("Erro", "ID ou CPF já cadastrado. Use valores únicos.")
                return

            cursor = conexao.cursor()
            data_nascimento_formatada = formatar_data(entry_data_nascimento.get())
            data_cadastro_formatada = formatar_data(entry_data_cadastro.get())

            if data_nascimento_formatada and data_cadastro_formatada:
                # Inserir dados na tabela
                query = """INSERT INTO cadastro_de_aluno (id, nome, data_nascimento, cpf, data_cadastro, nome_do_responsavel, email_do_responsavel) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    entry_id.get(),
                    entry_nome.get(),
                    data_nascimento_formatada,
                    entry_cpf.get(),
                    data_cadastro_formatada,
                    entry_nome_responsavel.get(),
                    entry_email_responsavel.get()
                )
                
                cursor.execute(query, valores)
                conexao.commit()

                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Criar a janela principal
janela = tk.Tk()
janela.title("Cadastro de Aluno")

# Caixa de texto para ID
label_id = tk.Label(janela, text="ID:")
label_id.grid(row=0, column=0)
entry_id = tk.Entry(janela)
entry_id.grid(row=0, column=1)

# Caixa de texto para nome
label_nome = tk.Label(janela, text="Nome:")
label_nome.grid(row=1, column=0)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=1, column=1)

# Caixa de texto para data de nascimento
label_data_nascimento = tk.Label(janela, text="Data de Nascimento (DD/MM/YYYY):")
label_data_nascimento.grid(row=2, column=0)
entry_data_nascimento = tk.Entry(janela)
entry_data_nascimento.grid(row=2, column=1)

# Caixa de texto para CPF
label_cpf = tk.Label(janela, text="CPF:")
label_cpf.grid(row=3, column=0)
entry_cpf = tk.Entry(janela)
entry_cpf.grid(row=3, column=1)

# Caixa de texto para data de cadastro
label_data_cadastro = tk.Label(janela, text="Data de Cadastro (DD/MM/YYYY):")
label_data_cadastro.grid(row=4, column=0)
entry_data_cadastro = tk.Entry(janela)
entry_data_cadastro.grid(row=4, column=1)

# Caixa de texto para nome do responsável
label_nome_responsavel = tk.Label(janela, text="Nome do Responsável:")
label_nome_responsavel.grid(row=5, column=0)
entry_nome_responsavel = tk.Entry(janela)
entry_nome_responsavel.grid(row=5, column=1)

# Caixa de texto para email do responsável
label_email_responsavel = tk.Label(janela, text="Email do Responsável:")
label_email_responsavel.grid(row=6, column=0)
entry_email_responsavel = tk.Entry(janela)
entry_email_responsavel.grid(row=6, column=1)

# Botão de cadastrar
botao_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_aluno)
botao_cadastrar.grid(row=7, column=1)

# Executar o loop da interface gráfica
janela.mainloop()

