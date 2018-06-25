# coding: utf-8

"""
    接口
"""

from flask import request, render_template, Response
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import *
from constant import UPLOAD_DIR, GET_APP_ID_URL, FEATURE_TRANS
from face_reading_svm import apply
from json_objs import Node, Result
from db import db
from models import *
import emotion_gender_processor as eg_processor
import flask_restless
import cv2
import json
import requests
import logging


def create_view(app, db):
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app, size=64*1024*1024)  # 设置最大文件大小，　size默认时64*1024*1024

    @app.route('/log', methods=['GET', 'POST'])
    def log_list():
        """
            log 的　list操作
        :return:
        """
        # 查看所有日志
        if request.method == "GET":
            page = request.args.get("page", 0, int)
            logs = Log.query.order_by(Log.op_time.desc()).paginate(page, per_page=10, error_out=False)
            return Response(json.dumps(logs.items, cls=ModelEncoder), mimetype="application/json")
        # 提交一条日志
        elif request.method == "POST":
            if request.get_json() is not None: # 小程序请求方式
                json_dict = request.get_json()
                json_dict.setdefault(" ")
                openid=json_dict.get('openid')
                op_content=json_dict.get("op_content")
                op_type=json_dict.get("op_type")
                remark=json_dict.get("remark")
            else:   # 普通post请求方式
                openid = request.form.get('openid')
                op_content = request.form.get("op_content", default=" ")
                op_type = request.form.get("op_type", default=" ")
                remark = request.form.get("remark", default=" ")

            log_obj = Log(openid=openid, op_content=op_content, op_type=op_type, remark=remark)
            db.session.add(log_obj)
            db.session.flush()
            db.session.refresh(log_obj)
            db.session.commit()
            return Response(json.dumps(log_obj.to_dict()), mimetype="application/json")
        else:
            pass

    @app.route('/log/<int:id>', methods=['GET', 'DELETE'])
    def log(id=-1):
        log_obj = Log.query.get(id)
        return Response(json.dumps(log_obj.to_dict()), mimetype="application/json")

    @app.route("/facestory_tag", methods=["GET", "POST"])
    def facestory_tag_list():
        # 查看tag
        if request.method == "GET":
            openid = request.args.get("openid")
            print(openid)
            if openid is not None:
                tags = FaceStoryTag.query.filter_by(openid=openid).order_by(FaceStoryTag.id).all()
            else:
                tags = FaceStoryTag.query.order_by(FaceStoryTag.id).all()
            return Response(json.dumps(tags, cls=ModelEncoder), mimetype="application/json")
        elif request.method == "POST":
            # 添加一个家属朋友用户
            if request.get_json() is not None:
                json_dict = request.get_json()
                json_dict.setdefault(" ")

                tag = FaceStoryTag(
                    name=json_dict.get("name"),
                    openid=json_dict.get("openid"),
                    gender=json_dict.get("gender"),
                    birth=json_dict.get("birth")
                )
                db.session.add(tag)
                db.session.flush()
                db.session.commit()
                return Response(json.dumps(tag.to_dict()), mimetype="application/json")


    @app.route("/facestory_tag/<int:id>", methods=['GET', 'DELETE', 'UPDATE'])
    def facestory_tag(id):
        facestory_tag_obj = FaceStoryTag.query.get(id)
        if request.method == 'GET':
            return Response(json.dumps(facestory_tag_obj), mimetype="application/json")
        elif request.method == 'DELETE':
            db.session.delete(facestory_tag_obj)
            db.session.commit()
            return Response(json.dumps({"code": 0, "message": "删除成功"}), mimetype='application/json')
        elif request.method == 'UPDATE':
            return Response(json.dumps(facestory_tag_obj), mimetype="application/json")
        else:
            pass

    @app.route('/user_info', methods=['GET', 'POST'])
    def user_info():
        res = dict()
        if request.method == 'GET':
            openid = request.args.get('openid')
            user_info = UserInfo.query.filter_by(openid=openid).first()
            if user_info is not None:
                res = user_info.to_dict()

        elif request.method == 'POST':
            # '{"nickName":"我不是大哥","gender":1,"language":"zh_CN","city":"Xinzhou","province":"Shanxi","country":"China","avatarUrl":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eokAGkics0CTDoLhUsukAmy4sTvb167M3kBKyGfYmBv0tj5InBiahpqhgXBaWic1Bz3OYXC2oYHCzNvg/132"}'
            if request.get_data() is not None:  # wx小程序请求格式

                json_data = str(request.get_data(), encoding="utf-8")
                json_dict = json.loads(json_data)
                json_dict.setdefault("")

                openid = json_dict.get('openid')
                nick_name = json_dict.get('nickName')
                avatar_url = json_dict.get('avatarUrl')
                gender = json_dict.get('gender')
                language = json_dict.get('language')
                province = json_dict.get('province')
                country = json_dict.get('country')
                city = json_dict.get('city')

            else:   # 普通post请求格式
                openid = request.form.get("openid")
                nick_name = request.form.get("nick_name")
                gender = str(request.form.get("gender", type=int, default=0))
                language = request.form.get("language")
                city = request.form.get("city")
                province = request.form.get("province")
                country = request.form.get("country")
                avatar_url = request.form.get("avatar_url")

            user_info_obj = UserInfo.query.filter_by(openid=openid).first()
            if user_info_obj is not None:   # 如果在数据库中已经有记录，则更新记录
                user_info_obj.nick_name = nick_name
                user_info_obj.gender = gender
                user_info_obj.language = language
                user_info_obj.city = city
                user_info_obj.province = province
                user_info_obj.country = country
                user_info_obj.avartar_url = avatar_url
            else:
                # 新建用户
                user_info_obj = UserInfo(openid, nick_name, gender, language, city, country, avatar_url)
            tag_obj = FaceStoryTag.query.filter_by(openid=openid).first()
            if tag_obj is None:
                tag_obj = FaceStoryTag("我的", openid=openid)
                db.session.add(tag_obj)
            db.session.add(user_info_obj)
            db.session.commit()
            res = user_info_obj.to_dict()
        else:
            pass
        return Response(json.dumps(res), mimetype='application/json')

    @app.route('/detect', methods=['POST'])
    def upload():
        """
            上传图片，并返回识别结果
        :return:
        """
        res = dict()
        res['data'] = 1

        filename = photos.save(request.files['photo'])
        # 获取原始图片
        unchanged_image = cv2.imread(UPLOAD_DIR + "/" + filename)

        if unchanged_image is None:
            abort(500, "不支持的图片")

        # 获取情绪，性别信息
        face_size, gender, emotion = eg_processor.process_image(unchanged_image)

        results = []

        # 情绪
        result = Result(title="情绪", detail=Node(
            contents=[
                Node(contents=[emotion], dtype="text", style="padding-top:10px").to_dict()
            ]
        ).to_dict()).to_dict()
        results.append(result)

        # 面部特征结果
        face_detail = list()
        face_detail_dict = apply(unchanged_image)
        if face_detail_dict is None:
            abort(500, "没有找到人脸")
        print(face_detail_dict.keys())
        for k in face_detail_dict.keys():
            print(face_detail_dict[k])
            face_detail.append(Node(
                contents=[str(face_detail_dict[k]['type']) + "\n" + str(face_detail_dict[k]['detail'])],
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

        res['face_size'] = face_size
        res['results'] = results
        res['image_url'] = photos.url(filename)

        story_json = json.dumps(res)

        openid = request.args.get("openid")
        print(openid)
        if openid is not None:
            # 保存记录到数据库
            print("保存用户记录到数据库" + openid)
            print(UserInfo.query.all())
            user_info = UserInfo.query.filter_by(openid=openid).first()
            print(user_info)
            if user_info is not None:
                story = FaceStory(openid, user_info.nick_name, user_info.avatar_url, story_json)

                tag = FaceStoryTag.query.filter(FaceStoryTag.openid==openid, FaceStoryTag.name=="我的").first()
                if tag is not None:
                    tag.face_story.append(story)
                    db.session.add(tag)
                db.session.add(story)
                db.session.flush()
                db.session.refresh(story)
                db.session.commit()
                return Response(json.dumps(story.to_dict()), mimetype='application/json')

        # return Response(story_json, mimetype='application/json')

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
        """
            返回用户的openid code 请求完之后失效
        :return:
        """
        code = request.args.get("code")
        logging.info(code)
        req = requests.get(GET_APP_ID_URL + code)
        return Response(req.content, mimetype='application/json')

    @app.route('/facestory', methods=['GET'])
    def facestory_list():
        if request.method == "GET":
            storys = []
            in_square = request.args.get("in_square")
            top = request.args.get("top")
            print(in_square, top, request.args.to_dict())
            if in_square is not None:
                # 获取广场
                in_square = True if int(in_square)==1 else False
                print(in_square)
                storys = FaceStory.query.filter(FaceStory.in_square==in_square, FaceStory.is_deleted==False).all()
            elif top is not None:
                # 获取排行榜
                print(int(top))
                storys = FaceStory.query.filter(
                    FaceStory.is_deleted==False, FaceStory.in_square==True
                ).order_by(FaceStory.like_num).limit(int(top)).all()
            else:
                storys = FaceStory.query.all()
            return Response(json.dumps(storys, cls=ModelEncoder), mimetype="application/json")
        else:
            pass

    @app.route('/facestory/<int:id>', methods=['GET', 'DELETE', 'UPDATE'])
    def story(id):
        """
            获取某个自拍记录
        :return:
        """
        story = FaceStory.query.get(id)
        if story is None:
            return
        if request.method == 'GET':
            res = story.to_dict()
            return Response(json.dumps(res), mimetype='application/json')
        elif request.method == 'DELETE':
            db.session.delete(story)
            db.session.commit()
            return Response(json.dumps({"code":0, "message":"删除成功"}), mimetype='application/json')
        elif request.method == "UPDATE":
            tag = request.args.get("tag")
            in_square = request.args.get("in_square")
            if tag is not None:
                story.tag = tag
            if in_square is not None:
                story.in_square = in_square
            db.session.commit()
            return Response(json.dumps(story.to_dict()), mimetype='application/json')

    @app.route('/share_to_square', methods=['GET'])
    def share_to_square():
        """
            分享到广场
        :return:
        """
        res = dict()
        story_id = request.args.get('id')
        in_square = request.args.get('in_square')
        story = FaceStory.query.filter_by(id=story_id).first()
        if story is not None:
            if int(in_square) == 0:
                story.in_square = False
                print("撤回")
            else:
                story.in_square = True
                print("分享")
            db.session.add(story)
            db.session.flush()
            db.session.refresh(story)
            db.session.commit()
            res = story.to_dict()
        return Response(json.dumps(res), mimetype='application/json')


    @app.errorhandler(500)
    def error500(error):
        """
            自定义错误用　abort(500, msg)　处理
        :param error:
        :return:
        """
        print(error)
        return Response(json.dumps({"code":-1, "message":str(error)}), mimetype="application/json")
    return app