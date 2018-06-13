# coding: utf-8

from db import db
from datetime import datetime
import json


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(40), unique=True)
    passwd = db.Column(db.String(40))  # password need to be hashed before installed

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id


class FaceStory(db.Model):
    """
        一个自拍记录
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信用户id
    openid = db.Column(db.VARCHAR(1024))
    # 昵称
    nick_name = db.Column(db.VARCHAR(256), nullable=False)
    # 用户头像
    avatar_url = db.Column(db.VARCHAR(1024), nullable=False)    # 这三个数据经常用到，这里冗余存起来

    # 日期
    date = db.Column(db.DateTime)
    # 自拍结果
    story_json = db.Column(db.TEXT)
    # 点赞
    like = db.Column(db.Integer, default=0)
    # 是否分享到广场
    in_square = db.Column(db.Boolean, default=False)

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['nick_name'] = self.nick_name
        d['avatar_url'] = self.avatar_url
        d['openid'] = self.openid
        d['story_json'] = json.loads(self.story_json)
        d['date'] = self.date.strftime("%Y-%m-%d %H:%M:%S")
        d['like'] = self.like
        d['in_square'] = self.in_square
        return d

    def __init__(self, openid, nick_name, avatar_url, story_json, like=0, in_square=False):
        self.openid = openid
        self.nick_name = nick_name
        self.avatar_url = avatar_url
        self.date = datetime.utcnow()
        self.story_json = story_json
        self.like = like
        self.in_square = in_square

    def __repr__(self) -> str:
        return "<FaceStory "+str(self.id)+self.openid+" "+self.nick_name+" "+str(self.date)+" "+str(self.like) + str(self.in_square)+">"


class UserInfo(db.Model):
    """
        存储用户信息，根据微信字段　
        "{"nickName":"我不是大哥","gender":1,"language":"zh_CN","city":"Xinzhou","province":"Shanxi","country":"China","avatarUrl":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eokAGkics0CTDoLhUsukAmy4sTvb167M3kBKyGfYmBv0tj5InBiahpqhgXBaWic1Bz3OYXC2oYHCzNvg/132"}"
    """
    # 微信的用户openid
    openid = db.Column(db.VARCHAR(256), primary_key=True)
    # 昵称
    nick_name = db.Column(db.VARCHAR(256), nullable=False)
    # 用户头像
    avatar_url = db.Column(db.VARCHAR(1024), nullable=False)
    # 性别
    gender = db.Column(db.CHAR(2), default="1", nullable=True)
    # 语言
    language = db.Column(db.VARCHAR(64), default="zh_CN", nullable=True)
    # 城市
    city = db.Column(db.VARCHAR(64), default="Xinzhou", nullable=True)
    # 国籍
    country = db.Column(db.VARCHAR(64), default="China", nullable=True)

    def to_dict(self):
        d = dict()
        d['openid'] = self.openid
        d['nick_name'] = self.nick_name
        d['avatar_url'] = self.avatar_url
        d['gender'] = self.gender
        d['language'] = self.language
        d['city'] = self.city
        d['country'] = self.country
        return d

    def __init__(self, openid, nick_name, gender, language, city, coutry, avatar_url):
        self.openid = openid
        self.nick_name = nick_name
        self.gender = gender
        self.language = language
        self.city = city
        self.country = coutry
        self.avatar_url = avatar_url

    def __repr__(self):
        return "<UserInfo "+self.nick_name+" "+self.openid+" >"
