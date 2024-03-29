# coding: utf-8
"""
    数据库定义

"""


from db import db
from datetime import datetime
import json


class User(db.Model):
    """
        用户后台管理登录
        默认用户　cisl cis-51355517
        pbkdf2:sha256:50000$AS9cAm2D$838abef9e7fbdf2c082a0657588bc0e639c48223f735c060888ade5d05057409
    """
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(40), unique=True)
    passwd = db.Column(db.String(40))

    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd

    # flask-login要求实现以下三个方法
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id


# 一对多关系
face_story_likes = db.Table('face_story_likes', db.Model.metadata,
                            db.Column('face_story_id', db.Integer, db.ForeignKey('face_story.id')),
                            db.Column('user_info_id', db.Integer, db.ForeignKey('user_info.id')))


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    """
        存储用户信息，根据微信字段　
        "{"nickName":"我不是大哥","gender":1,"language":"zh_CN","city":"Xinzhou","province":"Shanxi","country":"China","avatarUrl":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eokAGkics0CTDoLhUsukAmy4sTvb167M3kBKyGfYmBv0tj5InBiahpqhgXBaWic1Bz3OYXC2oYHCzNvg/132"}"
    """
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信的用户openid
    openid = db.Column(db.VARCHAR(256), unique=True)
    # 昵称
    nick_name = db.Column(db.VARCHAR(256), nullable=False, comment=u"昵称")
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

    def __init__(self, openid="", nick_name="", gender="", language="", city="", coutry="", avatar_url=""):
        self.openid = openid
        self.nick_name = nick_name
        self.gender = gender
        self.language = language
        self.city = city
        self.country = coutry
        self.avatar_url = avatar_url

    def __repr__(self):
        return "<UserInfo "+self.nick_name+" "+self.openid+" >"


class FaceStoryTag(db.Model):
    """
        标签
    """
    __tablename__ = "face_story_tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信的用户openid
    openid = db.Column(db.VARCHAR(256))
    name = db.Column(db.VARCHAR(256))
    gender = db.Column(db.VARCHAR(2), default="男")
    birth = db.Column(db.VARCHAR(16), default="1900-01-01")
    face_story = db.relationship('FaceStory', backref='face_story_tag')

    def __init__(self, name="", openid="", gender="男", birth="1900-01-01"):
        self.name = name
        self.openid = openid
        self.gender = gender
        self.birth = birth

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['openid'] = self.openid
        d['name'] = self.name
        d['gender'] = self.gender
        d['birth'] = self.birth
        d['face_storys'] = [s.to_dict() for s in self.face_story]
        return d

    def __repr__(self):
        return self.name


class FaceStory(db.Model):
    """
        一个自拍记录
    """
    __tablename__ = 'face_story'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信的用户openid
    openid = db.Column(db.VARCHAR(256))
    # 昵称
    nick_name = db.Column(db.VARCHAR(256), nullable=False)
    # 用户头像
    avatar_url = db.Column(db.VARCHAR(1024), nullable=False)    # 这三个数据经常用到，这里冗余存起来
    # 日期
    date = db.Column(db.DateTime)
    # 自拍结果
    story_json = db.Column(db.TEXT, default="")
    # 点赞
    likes = db.relationship('UserInfo', secondary=face_story_likes)
    # 电宰点赞数
    like_num = db.Column(db.Integer, default=0)
    # 标签
    tag = db.Column(db.Integer, db.ForeignKey('face_story_tag.id'))
    # 是否分享到广场
    in_square = db.Column(db.Boolean, default=False)
    # 是否已删除
    is_deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['nick_name'] = self.nick_name
        d['avatar_url'] = self.avatar_url
        d['openid'] = self.openid
        d['story_json'] = json.loads(self.story_json)
        d['date'] = self.date.strftime("%Y-%m-%d %H:%M:%S")
        d['like'] = [u.to_dict() for u in self.likes]
        d['like_num'] = self.like_num
        d['in_square'] = self.in_square
        d['is_deleted'] = self.is_deleted
        if self.tag is not None:
            tag = FaceStoryTag.query.get(self.tag)
            d['tag'] = {
                'name': tag.name,
                'id': tag.id
            }
        return d

    def __init__(self, openid="", nick_name="", avatar_url="", story_json="", in_square=False, is_deleted=False):
        self.openid = openid
        self.nick_name = nick_name
        self.avatar_url = avatar_url
        self.date = datetime.utcnow()
        self.story_json = story_json
        self.in_square = in_square
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return "<FaceStory "+str(self.id)+self.openid+" "+self.nick_name+" "+str(self.date)+" "+ str(self.in_square)+">"


class Log(db.Model):
    """
        用户操作日志
    """
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信的用户openid
    openid = db.Column(db.VARCHAR(256))
    # 操作类型
    op_type = db.Column(db.Integer(), default=0)
    # 操作内容
    op_content = db.Column(db.VARCHAR(256), nullable=False)
    # 操作时间
    op_time = db.Column(db.DateTime)
    # 备注
    remark = db.Column(db.VARCHAR(256), nullable=True)

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['openid'] = self.openid
        d['op_type'] = self.op_type
        d['op_content'] = self.op_content
        d['op_time'] = self.op_time.strftime('%Y-%m-%d %H:%M:%S')
        d['remark'] = self.remark
        return d

    def __init__(self, openid="", op_type=0, op_content="", remark=""):
        self.openid = openid
        self.op_type = op_type
        self.op_content = op_content
        self.op_time = datetime.utcnow()
        self.remark = remark

    def __repr__(self):
        return "<Log "+self.openid+" "+self.op_content+">"


class ModelEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, db.Model):
            return o.to_dict()
        return json.JSONEncoder.default(self, o)