from keras.models import load_model
import tensorflow as tf
import skimage.io as io
import os
from keras import backend as k
import uuid
from keras.models import Sequential
from PIL import Image
from resizeimage import resizeimage

class PredictHelper:
    def __init__(self):
        self.model = None

    def load_model(self, model_path):
        # get model from local storage and return it
        model = load_model(model_path)
        seq = Sequential()
        seq.add(model)
        seq.compile(loss='categorical_crossentropy', optimizer='adam')
        self.model = seq
        return seq

    def reshape_image(self, image):
        # reshape the image for the network and return it
        image_path = 'static/img/cache/' + str(uuid.uuid4()) + '.png'
        image.save(image_path)

        with open(image_path, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [224, 224])
                cover.save(image_path, image.format)

        image = io.imread(image_path, as_gray=False)
        image = image.astype('float32')
        image = image / 255
        image = image.reshape(-1, 224, 224, 3)

        return image, image_path

    def clear_session(self):
        if k.clear_session():
            return True
        else:
            return False