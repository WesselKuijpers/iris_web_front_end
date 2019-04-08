from keras.models import load_model
import tensorflow as tf
import skimage.io as io
import os
from keras import backend as k
import uuid
from keras.models import Sequential

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
        # TODO: make reshape size dependent on the model, or a variable
        image_name = uuid.uuid4()
        image.save('temp/' + str(image_name) + '.png')
        image = io.imread('temp/' + str(image_name) + '.png', as_gray=False)
        image = image.astype('float32')
        image = image / 255
        image = image.reshape(-1, 224, 224, 3)
        os.remove('temp/' + str(image_name) + '.png')
        return image

    def clear_session(self):
        if k.clear_session():
            return True
        else:
            return False