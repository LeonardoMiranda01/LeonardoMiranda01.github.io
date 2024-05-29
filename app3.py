from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app3 = Flask(__name__)

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="XXXXXX",
    database="banco-notas"
)
cursor = db.cursor()

# Rota para a página inicial
@app3.route('/')
def cadastro_materia():
    return render_template('cadastromateria.html')

# Rota para lidar com o formulário de envio
@app3.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        cod_materia = request.form['cod_materia']
        materia = request.form['materia']
        
        # Insere os dados no banco de dados
        cursor.execute("INSERT INTO materias (cod_materia, materia) VALUES (%s, %s)", (cod_materia, materia))
        db.commit()

        return redirect(url_for('cadastro_materia'))

if __name__ == '__main__':
    app3.run(debug=True)
