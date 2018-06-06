from db import db
from datetime import datetime
import json

class FaceStory(db.Model):
    """
        一个自拍记录
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信用户id
    openid = db.Column(db.VARCHAR(1024))
    # 日期
    date = db.Column(db.DateTime)
    # 自拍结果
    story_json = db.Column(db.TEXT)
    # 点赞
    like = db.Column(db.Integer, default=0)
    # 分享到广场
    in_square = db.Column(db.Boolean, default=False)

    def to_dict(self):
        d = dict()
        d['id'] = self.id
        d['openid'] = self.openid
        d['story_json'] = json.loads(self.story_json)
        d['date'] = self.date.strftime("%Y-%m-%d %H:%M:%S")
        d['like'] = self.like
        d['in_square'] = self.in_square
        return d

    def __init__(self, openid, story_json, like=0, in_square=False):
        self.openid = openid
        self.date = datetime.utcnow()
        self.story_json = story_json
        self.like = like
        self.in_square = in_square

    def __repr__(self) -> str:
        return "<FaceStory "+str(self.id)+self.openid+" "+str(self.date)+" "+str(self.like) + str(self.in_square)+">"