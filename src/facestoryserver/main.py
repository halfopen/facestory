# coding: utf-8
from flask import Flask
from constant import UPLOAD_DIR, DATA_BASE_URI,BASE_DIR
from views import create_view
from db import db
from admin import add_admin
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URI


db.init_app(app)
db.app = app
db.create_all()

app = create_view(app, db)
app = add_admin(app)

if User.query.first() is None:
    user = User("cisl", "pbkdf2:sha256:50000$AS9cAm2D$838abef9e7fbdf2c082a0657588bc0e639c48223f735c060888ade5d05057409")
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, ssl_context=(BASE_DIR+"/1_facestory.cn_bundle.crt",
                                                    BASE_DIR+"/2_facestory.cn.key"))
