# coding: utf-8
from flask import Flask
from constant import UPLOAD_DIR, DATA_BASE_URI
from views import create_view
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_DIR  # 文件上传路径
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URI

with app.app_context():
    db.init_app(app)
    db.create_all()
app = create_view(app, db)

if __name__ == '__main__':

    app.run(host='0.0.0.0')
