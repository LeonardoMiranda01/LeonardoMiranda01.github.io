from flask import Flask, render_template, request
import mysql.connector

app4 = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gustavo@2012',
    'database': 'banco-notas'
}

# Rota para a página inicial
@app4.route('/')
def consultarnota():
    return render_template('consultarnota.html')

# Rota para lidar com o formulário
@app4.route('/consultar_nota', methods=['POST'])
def consultar_nota():
    nome = request.form['nome']
    materia = request.form['materia']

    # Conectar ao banco de dados
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Consulta para calcular a média das notas do aluno na matéria específica
    query = """
            SELECT AVG(primeiro_bimestre) AS primeiro_bimestre_media,
                   AVG(segundo_bimestre) AS segundo_bimestre_media,
                   AVG(terceiro_bimestre) AS terceiro_bimestre_media,
                   AVG(quarto_bimestre) AS quarto_bimestre_media
            FROM notas
            WHERE nome = %s AND materia = %s
            """
    cursor.execute(query, (nome, materia))
    media_notas = cursor.fetchone()

    cursor.close()
    connection.close()

    notas = [media_notas[0], media_notas[1], media_notas[2], media_notas[3]]
    media_final = sum(notas) / 4

    return render_template('resultado.html', materia=materia, nome=nome, notas=notas, media=media_final)

if __name__ == '__main__':
    app4.run(debug=True)
