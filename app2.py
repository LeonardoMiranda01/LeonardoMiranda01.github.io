from flask import Flask, render_template, request
import mysql.connector

app2 = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'XXXXXXX',
    'database': 'banco-notas'
}

# Rota principal
@app2.route('/')
def registronotas():
    return render_template('registronotas.html')

# Rota para submissão do formulário
@app2.route('/submit', methods=['POST'])
def submit():
    # Obtendo os dados do formulário
    nome = request.form['nome']
    registroaluno = request.form['registroaluno']
    materia = request.form['materia']
    primeiro_bimestre = request.form['primeiro_bimestre']
    segundo_bimestre = request.form['segundo_bimestre']
    terceiro_bimestre = request.form['terceiro_bimestre']
    quarto_bimestre = request.form['quarto_bimestre']

    # Conexão com o banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query para inserir os dados na tabela notas
    insert_query = "INSERT INTO notas (nome, registroaluno, materia, primeiro_bimestre, segundo_bimestre, terceiro_bimestre, quarto_bimestre) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (nome, registroaluno, materia, primeiro_bimestre, segundo_bimestre, terceiro_bimestre, quarto_bimestre)

    try:
        # Executando a query de inserção
        cursor.execute(insert_query, data)
        # Commit das alterações no banco de dados
        conn.commit()
        # Fechando conexão
        cursor.close()
        conn.close()
        return 'Dados inseridos com sucesso!'
    except Exception as e:
        return f"Erro ao inserir dados: {str(e)}"

if __name__ == '__main__':
    app2.run(debug=True)
