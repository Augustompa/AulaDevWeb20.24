import mysql.connector
import sqlite3
from flask import Flask, request, jsonify

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('pizzariaAndorinhas.db')
c = conn.cursor()

# Criando a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sabor INTEGER,
    tamanho TEXT
)''')


class MySQLDB:
    def __init__(self, host, user, password, dbname):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.dbname
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, table, columns, values):
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(columns), ', '.join(['%s'] * len(values)))
        self.cursor.execute(query, values)
        self.conn.commit()

    def read_data(self, table, columns=None):
        if columns is None:
            query = "SELECT * FROM {}".format(table)
        else:
            query = "SELECT {} FROM {}".format(', '.join(columns), table)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table, set_columns_values, where_column, where_value):
        set_query = ', '.join(['{}=%s'.format(col) for col in set_columns_values])
        query = "UPDATE {} SET {} WHERE {}=%s".format(table, set_query, where_column)
        self.cursor.execute(query, set_columns_values + (where_value,))
        self.conn.commit()

    def delete_data(self, table, where_column, where_value):
        query = "DELETE FROM {} WHERE {}=%s".format(table, where_column)
        self.cursor.execute(query, (where_value,))
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        
        
        
how can I expose this class to consume in an page javascript?
// This code is generated using model Mixtral 8x7b Instruct 
To expose this class to be consumed in a page's JavaScript, you can create a REST API using a web framework like Flask or Django in Python. Here's an example using Flask:

1. Install Flask:

```bash
pip install Flask
```

2. Create a new Python script (`app.py`) and add the following code:

```python
from flask import Flask, request, jsonify
import mysql_crud

app = Flask(__name__)
db = mysql_crud.MySQLDB('localhost', 'user', 'password', 'database_name')

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    table = data.get('table')
    columns = data.get('columns')
    values = data.get('values')
    db.insert_data(table, columns, values)
    return jsonify({'message': 'Data inserted successfully'})

@app.route('/read/<string:table>', methods=['GET'])
def read_data(table):
    columns = request.args.get('columns')
    data = db.read_data(table, columns.split(',')) if columns else db.read_data(table)
    return jsonify(data)

@app.route('/update/<string:table>', methods=['PUT'])
def update_data(table):
    data = request.get_json()
    set_columns_values = data.get('set')
    where_column = data.get('where_column')
    where_value = data.get('where_value')
    db.update_data(table, set_columns_values, where_column, where_value)
    return jsonify({'message': 'Data updated successfully'})

@app.route('/delete/<string:table>', methods=['DELETE'])
def delete_data(table):
    data = request.get_json()
    where_column = data.get('where_column')
    where_value = data.get('where_value')
    db.delete_data(table, where_column, where_value)
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
```

3. Replace `'localhost'`, `'user'`, `'password'`, and `'database_name'` with your MySQL database credentials.

4. Run the Flask app:

```bash
python app.py
```

5. Now you can consume the API in your JavaScript code using the Fetch API or any HTTP client library like Axios.

For example, using the Fetch API:

```javascript
// Insert data


// Read data
fetch('http://localhost:5000/read/table_name?columns=column1,column2')
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));

// Update data
fetch('http://localhost:5000/update/table_name', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    set: {
      column1: 'new_value1',
      column2: 'new_value2'
    },
    where_column: 'id',
    where_value: 1
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));

// Delete data
fetch('http://localhost:5000/delete/table_name', {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    where_column: 'id',
    where_value: 1
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
```

Make sure to replace the table names, column names, and values with your own data.


