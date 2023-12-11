import streamlit as st
import numpy as np
import cv2
import os

from model import load_model
from mtcnn import MTCNN

from streamlit_extras.grid import grid


def run(file: str or bytearray):
    if type(file) == str:
        cv_image = cv2.imread('samples/' + file)
    else:
        cv_image = cv2.imdecode(file, 1)
    
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
    faces = face_detector.detect_faces(cv_image)
    people = []

    for face in faces:
        x, y, w, h = face['box']
        cropped_face = cv_image.copy()
        cropped_face = cropped_face[y:y+h, x:x+w]
        
        batch = np.expand_dims(cv2.resize(cropped_face, (128, 128)), axis=0)
        pred = gender_classifier.predict(batch)
        label = np.argmax(pred)
        gender = 'Rosto Masculino' if label == 0 else 'Rosto Feminino'

        people.append({'gender': gender, 'confidence':pred[0][label], 'face': cropped_face})
    
    for face in faces:
        x, y, w, h = face['box']
        cv_image = cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), thickness=4)    
    
    main_grid = grid([0.5, 0.5])
    with main_grid.container():
        st.subheader("Foto original 📷")
        image_grid = grid(1)
        image_grid.image(cv_image, use_column_width=True)
    
    with main_grid.container():
        st.subheader("Rostos detectados 👨🏼‍🦲")
        faces_grid = grid([0.3, 0.7])
        
        for person in people:
            faces_grid.image(person['face'], width=150)
            faces_grid.subheader("""{g}\n{c:.2f}% de certeza"""
                            .format(g=person['gender'], c=person['confidence']*100))


gender_classifier = load_model()
face_detector = MTCNN()

st.set_page_config(layout="wide")
st.title("Face Analyser 🔎👦🏽")
st.divider()

bttns = []
files = []
with st.sidebar:
    st.title("Envie uma foto, ou escolha um dos exemplos abaixo")
    uploaded_file = st.file_uploader("Envie uma foto para começar")
    st.divider()
    for file in os.listdir('samples'):
        files.append(file)
        st.image('samples/' + file)
        bttns.append(st.button('Usar imagem', key=file))

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    run(file_bytes)
else:
    for file in files:
        if st.session_state[file]:
            run(file)