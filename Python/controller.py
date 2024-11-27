from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

import sqlite3
import json

app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('pizzaria.db', check_same_thread=False)
c = conn.cursor()

# Criando a tabela de pizzas se não existir
c.execute('''CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    img TEXT,
    price DOUBLE,
    sabor TEXT,
    sizes ENUM,
    description TEXT

)''')


@app.route('/insertPizzas', methods=['POST'])
@cross_origin()
def adicionar_pizzas():

    try:
        data = request.json
        print("dataaaaa" + str(data))
        for item in data:
            print(item)
            
            varImg = item.get('img')
            print(varImg)
            varPrice = item.get('price')
            print(varPrice)
            varSabor = item.get('name')
            print(varSabor)
            varSizes = item.get('sizes')
            print(varSizes)
            varDescription = item.get('description')
            print(varDescription)
        
            conn.execute("INSERT INTO pizzas (img,price,sabor, sizes, description) VALUES (?, ?, ?, ?, ?)", (varImg, varPrice, varSabor, varSizes, varDescription))
        conn.commit()
            
    except sqlite3.IntegrityError as e:
        print("ENTROU NO ROLLBACK")
        conn.rollback()
        msg = "Error adding record: {e}"
        return jsonify({
            'message': 'Exception >>>' + msg
        })
    finally:
        conn.close()
        return jsonify({'message': 'Pizza adicionada com sucesso!',
                        'statusCode': 200
                        })


@app.route('/read', methods=['GET'])
@cross_origin()
def get_pizzas():
    
    with sqlite3.connect('pizzaria.db') as con:
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        data = cur.execute('SELECT * FROM pizzas')
        rows = cur.fetchall()
        result = []
        for row in rows:
            d = {}
            for i, col in enumerate(cur.description):
                d[col[0]] = row[i]
            result.append(d)

        # Convert the list of dictionaries to JSON and print it
        json_result = json.dumps(result)
        print(jsonify(json_result))
       
    return json_result
    
# @app.route('/update/<string:id>', methods=['PUT'])
# def update_data(table):
#     data = request.get_json()
#     idItem = data.get('id')
    
#     with sqlite3.connect('pizzaria.db') as con:
#         cur = con.cursor()
#         data = cur.execute('UPDATE pizzas SET WHERE id = ' + idItem)
        
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