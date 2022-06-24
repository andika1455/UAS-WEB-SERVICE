## ANDIKA DENNY PRADANA  - 19090145
## NU'MAL NURIL HAKIM    - 19090058

from flask import Flask, jsonify, request,make_response
import os, random, string
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    token = db.Column(db.String(225), unique=True, nullable=True)
db.create_all()

@app.route('/api/register', methods=['POST'])
def daftar():
    username = request.json['username']
    password = request.json['password']
    
    data = User(username=username, password=password)

    try:
        db.session.add(data)
        db.session.commit()
        result = jsonify({'msg': 'Registrasi sukses'}), 200, {'content-type': 'application/json'}
    except:
        result = jsonify({'msg': 'Registrasi gagal, username sudah ada!'}), 422, {'content-type': 'application/json'}

    return result

@app.route('/api/v1/login', methods=['POST'])
def masuk():
    username = request.json['username']
    password = request.json['password']
    
    account = User.query.filter_by(username=username, password=password)
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    if account.first():
        account.update({'token': token})
        db.session.commit()
        result = jsonify({'msg': 'Login berhasil!!', 'token': token}),  200, {'content-type': 'application/json'}
    else:
        result = jsonify({'msg': 'Login gagal'}),  401, {'content-type': 'application/json'}

    return result

@app.route('/api/v2/users/info', methods=['POST'])
def info_pengguna():
    dataToken = request.json['token']
    akun = User.query.filter_by(token=dataToken).first()
    if akun:
        return akun.username 
    else:
        return 'Token yang anda masukkan salah'
        
if __name__ == '__main__':
    app.run(debug=True, port=4000)