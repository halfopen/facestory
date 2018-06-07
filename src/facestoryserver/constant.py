# coding: utf-8
import os

# 当前目录
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# 图片上传目录
UPLOAD_DIR = BASE_DIR+"/static/uploads"
# 数据库地址
DATA_BASE_URI = 'sqlite:///'+BASE_DIR+'/facestory.db'
# 面部检测模型地址
detection_model_path = BASE_DIR + '/trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = BASE_DIR + '/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = BASE_DIR + '/trained_models/gender_models/simple_CNN.81-0.96.hdf5'
# 面相模型地址
svm_model_path = BASE_DIR + '/trained_models/face_reading/trained_svms.pkl'
LANDMARK_PATH = BASE_DIR+"/trained_models/face_reading/shape_predictor_68_face_landmarks.dat"

analysis_json_path = BASE_DIR + '/trained_models/face_reading/analysis.json'
# 微信小程序appid
APP_ID = 'wx4b425b0c87a891b7'
# 微信小程序secret
SECRET = '83e750ced5f0ead5ca0c2a6bbd0051cd'
# openid接口
GET_APP_ID_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + APP_ID + '&secret=' + SECRET + '&grant_type=authorization_code&js_code='