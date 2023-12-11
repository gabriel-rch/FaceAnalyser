from keras.models import Sequential
from keras import layers
from keras.applications import VGG16
import gdown
import os.path

def load_model() -> Sequential:
    model = Sequential()

    base_model = VGG16(
        include_top=False,
        weights='imagenet',
        input_shape=(128, 128, 3))

    base_model.trainable = False

    model.add(base_model)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.Dense(2, activation='softmax'))

    if not os.path.isfile('weights.h5'):
        download_weights()
    model.load_weights('weights.h5')
    return model

def download_weights():
    gdown.download('https://drive.google.com/uc?export=download&id=106elrm-hmKUJcaAeBK6MGcMZOAFYvaLi', 'weights.h5')