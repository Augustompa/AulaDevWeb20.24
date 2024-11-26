from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('pizzaria.db', check_same_thread=False)
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

    try:
        data = request.get_json()
        print(data)
        varNome = data.get('Nome')
        varSabor = data.get('Sabor')
        varTamanho = data.get('Tamanho')
        varValor = data.get('Valor')  
    
        c.execute("INSERT INTO pizzas (nome,sabor,tamanho,valor) VALUES (?, ?, ?, ?)", (varNome, varSabor, varTamanho, varValor))
        c.commit()
        msg = "Record successfully added to database"
            
    except sqlite3.IntegrityError as e:
        print("ENTROU NO ROLLBACK")
        c.rollback()
        msg = "Error adding record: {e}"

    finally:
        c.close()
        return jsonify({'message': 'Pizza adicionada com sucesso!',
                        'statusCode': 200
                        })


@app.route('/read', methods=['GET'])
def get_pizzas():
    
    with sqlite3.connect('pizzaria.db') as con:
        cur = con.cursor()
    data = cur.execute('SELECT * FROM pizzas')
    return jsonify({
            "data": data.fetchall()
    })

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
    app.run(port=5000, host='localhost',debug=True)