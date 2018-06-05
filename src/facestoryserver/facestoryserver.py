# coding: utf-8
from flask import Flask, render_template,request, abort, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileStorage
from wtforms import SubmitField
import numpy as np
import os, json, logging
import cv2

from constant import *
import emotion_gender_processor as eg_processor
from face_reading_svm import apply

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_DIR

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

    logging.info(request.files['photo'])
    filename = photos.save(request.files['photo'])
    # 获取原始图片
    unchanged_image = cv2.imread(UPLOAD_DIR+"/"+filename)

    #
    face_size, gender, emotion = eg_processor.process_image(unchanged_image)

    response_obj['face_reading'] = apply(unchanged_image)
    response_obj['face_size'] = face_size
    response_obj['emotion'] = emotion
    response_obj['gender'] = gender
    response_obj['image_url'] = photos.url(filename)
    return jsonify(response_obj)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    class UploadForm(FlaskForm):
        photo = FileField(validators=[
            FileAllowed(photos, u'只能上传图片！'),
            FileRequired(u'文件未选择！')])
        submit = SubmitField(u'上传')
    form = UploadForm()
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
