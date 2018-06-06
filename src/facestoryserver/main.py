# coding: utf-8
from flask import Flask
from constant import UPLOAD_DIR
from views import create_view
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_DIR  # 文件上传路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)
app = create_view(app, db)

if __name__ == '__main__':

    app.run(host='0.0.0.0')
