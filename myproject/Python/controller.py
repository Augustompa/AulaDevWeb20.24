from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('pizzariaAndorinhas.db', check_same_thread=False)
c = conn.cursor()

# Criando a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sabor INTEGER,
    tamanho TEXT,
    valor DOUBLE

)''')

@app.route('/insert', methods=['POST'])
def adicionar_usuario():

    cart = request.get_json()

    for itemCart in cart:
        varSabor = itemCart.item.name
        varTamanho = itemCart.size
        varValor = (itemCart.item.price)*itemCart.qt
        c.execute("INSERT INTO pizzas (nome,sabor,tamanho,valor) VALUES (?, ?, ?, ?)", (varSabor, varTamanho, varValor))
    
    conn.commit()

    return jsonify({'message': 'Pizza adicionada com sucesso!'})

@app.route('/read', methods=['GET'])
def get_pizzas():
    data = c.execute('SELECT * FROM pizzas')
    return jsonify({data})

# @app.route('/update/<string:table>', methods=['PUT'])
# def update_data(table):
#     data = request.get_json()
#     set_columns_values = data.get('set')
#     where_column = data.get('where_column')
#     where_value = data.get('where_value')
#     db.update_data(table, set_columns_values, where_column, where_value)
#     return jsonify({'message': 'Data updated successfully'})

# @app.route('/delete/<string:table>', methods=['DELETE'])
# def delete_data(table):
#     data = request.get_json()
#     where_column = data.get('where_column')
#     where_value = data.get('where_value')
#     db.delete_data(table, where_column, where_value)
#     return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

#FLASK_APP=controller.py FLASK_DEBUG=true flask run
