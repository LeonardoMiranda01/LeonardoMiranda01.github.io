from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="XXXXXXX",
    database="banco-notas"
)
cursor = db.cursor()

# Rota para a página inicial
@app.route('/')
def cadastroaluno():
    return render_template('cadastroaluno.html')

# Rota para lidar com o formulário de envio
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nome = request.form['nome']
        registroaluno = request.form['registroaluno']
        
        # Insere os dados no banco de dados
        cursor.execute("INSERT INTO alunos (nome, registroaluno) VALUES (%s, %s)", (nome, registroaluno))
        db.commit()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

