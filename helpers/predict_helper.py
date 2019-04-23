import os
import uuid

import skimage.io as io
import tensorflow as tf
from keras import backend as k
from keras.models import Sequential, load_model
from PIL import Image
from resizeimage import resizeimage
import keras.backend as K


class PredictHelper:
    def __init__(self):
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6, allow_growth=True)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        K.set_session(sess)

        self.model = None
        self.graph = None

    def load_model(self, model_path):
        # set the graph
        global graph
        graph = tf.get_default_graph()
        self.graph = graph

        # get the model from storage and return it
        model = load_model(model_path)
        seq = Sequential()
        seq.add(model)
        seq.compile(loss='categorical_crossentropy', optimizer='adam')
        self.model = seq
        return seq

    def reshape_image(self, image):
        # save the image from the request
        image_path = 'static/img/cache/' + str(uuid.uuid4()) + '.png'
        image.save(image_path)

        # resize the saved image and save it again
        with open(image_path, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [224, 224])
                cover.save(image_path, image.format)

        # read the image as a numpy array
        image = io.imread(image_path, as_gray=False)
        image = image.astype('float32')
        image = image / 255
        image = image.reshape(-1, 224, 224, 3)

        return image, image_path

    def clear_session(self):
        k.clear_session()
