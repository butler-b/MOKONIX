from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'exampleuser'
app.config['MYSQL_PASSWORD'] = 'examplepass'
app.config['MYSQL_DB'] = 'hospitaldb'

mysql = MySQL(app)

@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hospitals")
    results = cur.fetchall()
    cur.close()
    
    hospitals = []
    for row in results:
        hospitals.append({'id': row[0], 'name': row[1], 'address': row[2]})
    
    return jsonify(hospitals)

if __name__ == '__main__':
    app.run(debug=True)

