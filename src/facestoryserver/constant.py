# coding: utf-8
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIR = BASE_DIR+"/static/uploads"

detection_model_path = BASE_DIR + '/trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = BASE_DIR + '/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = BASE_DIR + '/trained_models/gender_models/simple_CNN.81-0.96.hdf5'

svm_model_path = BASE_DIR + '/trained_models/face_reading/trained_svms.pkl'
LANDMARK_PATH = BASE_DIR+"/trained_models/face_reading/shape_predictor_68_face_landmarks.dat"

analysis_json_path = BASE_DIR + '/trained_models/face_reading/analysis.json'


