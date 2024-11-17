import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Função para verificar se o aluno existe no banco
def verificar_aluno():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxxxxxxx'
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            query = "SELECT nome FROM cadastro_de_aluno WHERE id = %s"
            cursor.execute(query, (entry_id.get(),))
            resultado = cursor.fetchone()

            if resultado:
                entry_nome_aluno.delete(0, tk.END)
                entry_nome_aluno.insert(0, resultado[0])
            else:
                messagebox.showerror("Erro", "Aluno não registrado.")
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao verificar aluno: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para carregar as matérias
def carregar_materias():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxx'
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM materia")
            materias = cursor.fetchall()
            entry_materia['values'] = [materia[0] for materia in materias]
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar matérias: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para inserir notas
def inserir_notas():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxxxxxxx'
        )
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            query = """INSERT INTO notas (id_aluno, nome_aluno, serie, materia, nota_1_bimestre, nota_2_bimestre, nota_3_bimestre, nota_4_bimestre)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (
                entry_id.get(),
                entry_nome_aluno.get(),
                entry_serie.get(),
                entry_materia.get(),
                entry_nota1.get(),
                entry_nota2.get(),
                entry_nota3.get(),
                entry_nota4.get()
            )
            
            cursor.execute(query, valores)
            conexao.commit()

            messagebox.showinfo("Sucesso", "Notas inseridas com sucesso!")
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao inserir notas: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Criar a janela principal
janela = tk.Tk()
janela.title("Cadastro de Notas")

# Campo de texto para ID do aluno
label_id = tk.Label(janela, text="ID do Aluno:")
label_id.grid(row=0, column=0)
entry_id = tk.Entry(janela)
entry_id.grid(row=0, column=1)

# Botão para verificar aluno
botao_verificar = tk.Button(janela, text="Verificar Aluno", command=verificar_aluno)
botao_verificar.grid(row=0, column=2)

# Campo de texto para nome do aluno
label_nome_aluno = tk.Label(janela, text="Nome do Aluno:")
label_nome_aluno.grid(row=1, column=0)
entry_nome_aluno = tk.Entry(janela)
entry_nome_aluno.grid(row=1, column=1)

# Campo de seleção de matéria
label_materia = tk.Label(janela, text="Matéria:")
label_materia.grid(row=2, column=0)
entry_materia = ttk.Combobox(janela)
entry_materia.grid(row=2, column=1)
carregar_materias()

# Campo para série
label_serie = tk.Label(janela, text="Série:")
label_serie.grid(row=3, column=0)
entry_serie = tk.Entry(janela)
entry_serie.grid(row=3, column=1)

# Campos para as notas dos 4 bimestres
label_nota1 = tk.Label(janela, text="Nota 1º Bimestre:")
label_nota1.grid(row=4, column=0)
entry_nota1 = tk.Entry(janela)
entry_nota1.grid(row=4, column=1)

label_nota2 = tk.Label(janela, text="Nota 2º Bimestre:")
label_nota2.grid(row=5, column=0)
entry_nota2 = tk.Entry(janela)
entry_nota2.grid(row=5, column=1)

label_nota3 = tk.Label(janela, text="Nota 3º Bimestre:")
label_nota3.grid(row=6, column=0)
entry_nota3 = tk.Entry(janela)
entry_nota3.grid(row=6, column=1)

label_nota4 = tk.Label(janela, text="Nota 4º Bimestre:")
label_nota4.grid(row=7, column=0)
entry_nota4 = tk.Entry(janela)
entry_nota4.grid(row=7, column=1)

# Botão para inserir notas
botao_inserir = tk.Button(janela, text="Inserir Notas", command=inserir_notas)
botao_inserir.grid(row=8, column=1)

# Executar o loop da interface gráfica
janela.mainloop()
