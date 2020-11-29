import dlib
import numpy as np
from PIL import Image
import requests
from io import BytesIO


face_detector = dlib.get_frontal_face_detector()
face_detector2 = dlib.cnn_face_detection_model_v1('dlib-models/mmod_human_face_detector.dat')
face_encoder = dlib.face_recognition_model_v1('dlib-models/dlib_face_recognition_resnet_model_v1.dat')
shape_predictor = dlib.shape_predictor('dlib-models/shape_predictor_68_face_landmarks.dat')


load_img = lambda x: np.array(Image.open(x).convert('RGB'))


def url_to_img(url: str):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return np.array(img)


vector_to_str = lambda arr: ', '.join(str(x) for x in arr)
vector_to_list = lambda arr: list(float(x) for x in arr)


def get_encod(img):
    if isinstance(img, str):
        img = load_img(img)
    face_rectangle = face_detector(img, 1)
    landmarks = shape_predictor(img, face_rectangle[0])
    embedding = face_encoder.compute_face_descriptor(img, landmarks, num_jitters=10)
    return np.asarray(embedding)


distance = lambda a, b: np.linalg.norm(a - b)
