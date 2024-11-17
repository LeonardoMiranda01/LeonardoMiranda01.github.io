import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para enviar o e-mail
def enviar_email():
    try:
        # Conectar ao banco para obter o email do responsável e o nome do aluno
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxx'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            
            # Query para obter o nome do aluno e o email do responsável da tabela cadastro_de_aluno
            query = "SELECT nome, email_do_responsavel FROM cadastro_de_aluno WHERE id = %s"
            cursor.execute(query, (entry_id_aluno.get(),))
            resultado = cursor.fetchone()

            if resultado:
                nome_aluno, email_do_responsavel = resultado
                serie = entry_serie.get()  # Obter a série diretamente do campo de entrada
                
                # Montar o corpo do e-mail com as notas
                corpo_email = f"Prezado responsável,\n\nSegue abaixo as notas do aluno {nome_aluno} (Série: {serie}):\n\n"
                for row in tabela.get_children():
                    item = tabela.item(row)['values']
                    materia, nota1, nota2, nota3, nota4 = item
                    corpo_email += f"{materia} - 1º Bimestre: {nota1}, 2º Bimestre: {nota2}, 3º Bimestre: {nota3}, 4º Bimestre: {nota4}\n"
                corpo_email += "\nAtenciosamente,\n\n[Nome da Escola]"

                # Configurações do e-mail
                msg = MIMEMultipart()
                msg['From'] = 'miranda.leonardoj@gmail.com'
                msg['To'] = email_do_responsavel
                msg['Subject'] = f"Notas: {nome_aluno}"
                msg.attach(MIMEText(corpo_email, 'plain'))

                # Configurar o servidor SMTP do Outlook
                with smtplib.SMTP('smtp.office365.com', 587) as server:
                    server.starttls()
                    server.login('miranda.leonardoj@gmail.com', 'Gustavo@2012')  # Altere para suas credenciais
                    server.sendmail(msg['From'], msg['To'], msg.as_string())

                messagebox.showinfo("Sucesso", f"E-mail enviado para {email_do_responsavel}")

            else:
                messagebox.showerror("Erro", "Não foi possível encontrar o e-mail do responsável para o ID informado.")
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar informações: {e}")
    
    except smtplib.SMTPException as e:
        messagebox.showerror("Erro", f"Erro ao enviar o e-mail: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para buscar e exibir as notas
def buscar_notas():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='teste',
            user='root',
            password='xxxxxxxxx'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            # Query para selecionar o nome do aluno e as notas
            query = """
            SELECT nome_aluno, materia, nota_1_bimestre, nota_2_bimestre, nota_3_bimestre, nota_4_bimestre 
            FROM notas 
            WHERE id_aluno = %s AND serie = %s
            """
            valores = (entry_id_aluno.get(), entry_serie.get())
            cursor.execute(query, valores)
            resultados = cursor.fetchall()

            for row in tabela.get_children():
                tabela.delete(row)

            # Exibir nome do aluno
            if resultados:
                nome_aluno = resultados[0][0]  # Nome do aluno na primeira coluna do primeiro resultado
                label_nome_aluno.config(text=f"Nome do Aluno: {nome_aluno}")
                
                # Inserir os dados na tabela, omitindo o nome do aluno em cada linha
                for row in resultados:
                    tabela.insert("", "end", values=row[1:])  # Exclui o nome_aluno do valor inserido

            else:
                label_nome_aluno.config(text="Nome do Aluno: Não encontrado")
                messagebox.showinfo("Informação", "Nenhuma nota encontrada para o ID e série informados.")
    
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar notas: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Interface gráfica
janela = tk.Tk()
janela.title("Consulta de Notas")

label_id_aluno = tk.Label(janela, text="ID do Aluno:")
label_id_aluno.grid(row=0, column=0, padx=5, pady=5)
entry_id_aluno = tk.Entry(janela)
entry_id_aluno.grid(row=0, column=1, padx=5, pady=5)

label_serie = tk.Label(janela, text="Série:")
label_serie.grid(row=1, column=0, padx=5, pady=5)
entry_serie = tk.Entry(janela)
entry_serie.grid(row=1, column=1, padx=5, pady=5)

# Rótulo para exibir o nome do aluno
label_nome_aluno = tk.Label(janela, text="Nome do Aluno: ")
label_nome_aluno.grid(row=2, column=0, columnspan=2, pady=5)

botao_buscar = tk.Button(janela, text="Buscar Notas", command=buscar_notas)
botao_buscar.grid(row=3, column=0, columnspan=2, pady=10)

botao_enviar_email = tk.Button(janela, text="Enviar E-mail", command=enviar_email)
botao_enviar_email.grid(row=4, column=0, columnspan=2, pady=10)

colunas = ("materia", "nota_1_bimestre", "nota_2_bimestre", "nota_3_bimestre", "nota_4_bimestre")
tabela = ttk.Treeview(janela, columns=colunas, show="headings")

for coluna in colunas:
    tabela.heading(coluna, text=coluna.replace('_', ' ').title())
    tabela.column(coluna, anchor="center")

tabela.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

janela.mainloop()
