# coding: utf-8

from flask_sqlalchemy import SQLAlchemy
# 把db单独放一个文件，避免main和views交叉引用
db = SQLAlchemy()
