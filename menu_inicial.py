import tkinter as tk
import subprocess
import pyttsx3
from PIL import Image, ImageTk  # Importando para exibir a imagem

# Inicializando o motor de TTS
engine = pyttsx3.init()

# Função para falar um texto
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# Função para abrir o módulo 'cadastro_aluno.py'
def abrir_cadastro_aluno():
    subprocess.run(['python', 'cadastro_aluno.py'])

# Função para abrir outros módulos (caso queira adicionar mais funcionalidades)
def abrir_materia():
    subprocess.run(['python', 'materia.py'])

def abrir_inserir_notas():
    subprocess.run(['python', 'inserir_notas.py'])

def abrir_consultar_nota():
    subprocess.run(['python', 'consulta_nota.py'])

# Função para descrever as funcionalidades
def descrever_funcionalidades():
    falar("Este aplicativo permite o cadastro de alunos. Clique em Cadastro de Aluno para iniciar o registro de um novo aluno. Clique em materária para registrar um nova matéria. Clique em Inserir notas para inserir novas notas dos alunos. Clique em consultar nota para consultar a nota dos alunos")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Tela Inicial")
janela.geometry("500x200")  # Tamanho da janela ajustado

# Mudando a cor de fundo da janela para azul claro
janela.configure(bg="#ADD8E6")  # Azul claro (Light Blue)

# Container para alinhar os botões à esquerda
frame_esquerdo = tk.Frame(janela, bg="#ADD8E6")  # Mantendo a cor de fundo
frame_esquerdo.pack(side=tk.LEFT, padx=20, pady=20)

# Padronizando o tamanho dos botões
button_width = 20  # Largura padrão para os botões

# Botão para o cadastro de alunos
btn_cadastro_aluno = tk.Button(frame_esquerdo, text="Cadastro de Aluno", command=abrir_cadastro_aluno, width=button_width)
btn_cadastro_aluno.pack(anchor='w', pady=10)

# Botão para outro módulo (opcional)
btn_outro_modulo = tk.Button(frame_esquerdo, text="Cadastro de Materia", command=abrir_materia, width=button_width)
btn_outro_modulo.pack(anchor='w', pady=10)

btn_outro_modulo = tk.Button(frame_esquerdo, text="Inserir notas", command=abrir_inserir_notas, width=button_width)
btn_outro_modulo.pack(anchor='w', pady=10)

btn_outro_modulo = tk.Button(frame_esquerdo, text="Consultar Nota", command=abrir_consultar_nota, width=button_width)
btn_outro_modulo.pack(anchor='w', pady=10)


# Exibindo a imagem à direita
frame_direito = tk.Frame(janela, bg="#ADD8E6")  # Mantendo a cor de fundo
frame_direito.pack(side=tk.RIGHT, padx=20, pady=20)

# Carregando a imagem
imagem = Image.open("imagem.png")
imagem = imagem.resize((300, 150), Image.LANCZOS)  # Aumentando o tamanho da imagem (300x150)
imagem_tk = ImageTk.PhotoImage(imagem)

# Label para mostrar a imagem
label_imagem = tk.Label(frame_direito, image=imagem_tk, bg="#ADD8E6")  # Mantendo a cor de fundo
label_imagem.pack()

# Botão para descrever funcionalidades no canto inferior direito e com tamanho pequeno
btn_descrever = tk.Button(janela, text="Descrição", command=descrever_funcionalidades, width=10)
btn_descrever.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posição do botão no canto inferior direito

# Executar a janela
janela.mainloop()
