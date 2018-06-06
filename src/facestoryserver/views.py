# coding: utf-8
from flask import request, render_template, Response
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import *
from constant import UPLOAD_DIR, GET_APP_ID_URL
from face_reading_svm import apply
from json_objs import Node, Result
from db import db
from models import FaceStory
import emotion_gender_processor as eg_processor
import cv2
import json
import requests
import logging


def create_view(app, db):

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)  # set maximum file size, default is 16MB

    @app.route('/detect', methods=['POST'])
    def upload():
        """
            上传图片，并返回识别结果
        :return:
        """
        response_obj = dict()
        response_obj['data'] = 1

        filename = photos.save(request.files['photo'])
        # 获取原始图片
        unchanged_image = cv2.imread(UPLOAD_DIR + "/" + filename)

        # 获取情绪，性别信息
        face_size, gender, emotion = eg_processor.process_image(unchanged_image)

        results = []
        # 面部特征结果
        face_detail = list()
        face_detail_dict = apply(unchanged_image)
        print(face_detail_dict.keys())
        for k in face_detail_dict.keys():
            face_detail.append(Node(
                contents=[face_detail_dict[k]['type'] + "\n" + face_detail_dict[k]['detail']],
                dtype="text",
                style="padding-top:10px").to_dict())

        result = Result(title="面部特征",
                        detail=Node(
                            contents=face_detail).to_dict()
                        ).to_dict()
        results.append(result)

        # 健康特征结果
        health_detail = list()
        health_detail.append(Node(style="padding-top:10px", dtype="text", contents=["1. 保健原则：益气固表，健脾和胃"]).to_dict())
        health_detail.append(Node(style="padding-top:10px", dtype="text",
                                  contents=["2. 起居养生：早睡早起，保证睡眠充足，四季起居有常；适度运动，避免过度体力劳动．"]).to_dict())
        health_detail.append(Node(style="padding-top:10px", dtype="text", contents=["3. 饮食药膳：现在是小满，我国古代将小满分为三候：\n“一候苦菜秀;二候靡草死;\
        三候麦秋至。”《周书》中，即有“小满之日苦菜秀”之说。小满时节的气候较为潮湿，所以适宜食用一些祛湿类的食物，如番茄，西瓜。"]).to_dict())
        health_detail.append(Node(dtype="image", contents=["/images/baidu/fanqie.jpeg"]).to_dict())
        health_detail.append(
            Node(dtype="text", contents=["这是最好的防晒食物。番茄富含抗氧化剂番茄红素，每天摄入16毫克番茄红素可将晒伤的危险系数下降40%。"]).to_dict())
        health_detail.append(Node(dtype="image", contents=["/images/baidu/xigua.jpg"]).to_dict())
        health_detail.append(Node(dtype="text", contents=["西瓜含水量在水果中是首屈一指的，所以特别适合补充人体水分的损失。"]).to_dict())

        health_result = Result(title="健康状况：气虚，肾虚", more="详细诊断 >",
                               detail=Node(contents=health_detail).to_dict()).to_dict()
        results.append(health_result)

        response_obj['face_size'] = face_size
        response_obj['results'] = results
        response_obj['image_url'] = photos.url(filename)

        story_json = json.dumps(response_obj)

        openid = request.args.get("openid")

        if openid is not None:
            # 保存记录到数据库
            logging.info("保存用户记录到数据库" + openid)
            story = FaceStory(openid, story_json)
            db.session.add(story)
            db.session.commit()
            pass

        return Response(story_json, mimetype='application/json')

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        """
            用于测试接口的html
        :return:
        """

        class UploadForm(FlaskForm):
            photo = FileField(validators=[
                FileAllowed(photos, u'只能上传图片！'),
                FileRequired(u'文件未选择！')])
            submit = SubmitField(u'上传')

        form = UploadForm()
        return render_template('index.html', form=form)

    @app.route('/get_openid', methods=['GET'])
    def get_openid():
        code = request.args.get("code")
        logging.info(code)
        req = requests.get(GET_APP_ID_URL + code)
        print(req.content)
        return Response(req.content, mimetype='application/json')

    return app