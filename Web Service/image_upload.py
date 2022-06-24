## ANDIKA DENNY PRADANA  - 19090145
## NU'MAL NURIL HAKIM    - 19090058

import datetime
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
app = Flask(__name__)

app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(
    os.path.join(app_dir, "upload.db"))
app.config['UPLOAD_FOLDER'] = 'img'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    file = db.Column(db.String(120), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
db.create_all()

@app.route('/uploadgambar', methods=['POST'])
def upload():

    name = request.form.get('name')
    file = request.files['file']

    if 'file' not in request.files:
        return jsonify({'msg': 'Upload Gagal'})

    if file.filename != '':
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = User(name=name, file=filename)
            db.session.add(data)
            db.session.commit()
            return jsonify({'msg': 'Upload Berhasil'})
        except Exception as error:
            return jsonify({'msg': 'Upload Gagal nama harus unik, nama ini '+name+' sudah dipakai!'})
    else:
        return jsonify({'msg': 'Upload Gagal'})


if __name__ == '__main__':
    app.run(debug=True)