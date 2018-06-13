import os
import sys
import logging

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels, get_emotion_lables
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input
from constant import *

import tensorflow as tf
g = tf.Graph()

with g.as_default():
    face_detection = load_detection_model(DETECTION_MODEL_PATH)
    emotion_classifier = load_model(EMOTION_MODEL_PATH, compile=False)
    gender_classifier = load_model(GENDER_MODEL_PATH, compile=False)

print("read face reading model end")

def process_image(unchanged_image):
    """

    :param unchanged_image:
    :return:
    """
    face_size = -1
    emotion = ''
    gender = ''
    try:
        # parameters for loading data and images

        emotion_labels = get_labels('fer2013')
        gender_labels = get_labels('imdb')
        font = cv2.FONT_HERSHEY_SIMPLEX

        # hyper-parameters for bounding boxes shape
        gender_offsets = (30, 60)
        gender_offsets = (10, 10)
        emotion_offsets = (20, 40)
        emotion_offsets = (0, 0)

        with g.as_default(): # 多次调用
            # loading models
            # getting input model shapes for inference
            emotion_target_size = emotion_classifier.input_shape[1:3]
            gender_target_size = gender_classifier.input_shape[1:3]

            rgb_image = cv2.cvtColor(unchanged_image, cv2.COLOR_BGR2RGB)
            gray_image = cv2.cvtColor(unchanged_image, cv2.COLOR_BGR2GRAY)

            faces = detect_faces(face_detection, gray_image)
            if len(faces)>=1:
                face_coordinates = faces[0]
                x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
                rgb_face = rgb_image[y1:y2, x1:x2]

                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]

                try:
                    rgb_face = cv2.resize(rgb_face, (gender_target_size))
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    pass

                rgb_face = preprocess_input(rgb_face, False)
                rgb_face = np.expand_dims(rgb_face, 0)
                gender_prediction = gender_classifier.predict(rgb_face)
                gender_label_arg = np.argmax(gender_prediction)
                gender_text = gender_labels[gender_label_arg]

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
                emotion_text = emotion_labels[emotion_label_arg]

                if gender_text == gender_labels[0]:
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)
                print(emotion_text, gender_text, len(faces))
                face_size = len(faces)
                gender = gender_text
                emotion = get_emotion_lables()[emotion_text]
    except Exception as err:
        logging.error('Error in emotion gender processor: "{0}"'.format(err))

    return face_size, gender, emotion
