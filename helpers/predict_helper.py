import os
import uuid

import skimage.io as io
import tensorflow as tf
from keras import backend as k
from keras.models import Sequential, load_model
from PIL import Image
from resizeimage import resizeimage


class PredictHelper:
    def __init__(self):
        self.model = None
        self.graph = None

    def load_model(self, model_path):
        # set the graph
        global graph
        graph = tf.get_default_graph()
        self.graph = graph

        # get the model from storage and return it
        model = load_model(model_path)
        # seq = Sequential()
        # seq.add(model)
        # seq.compile(loss='categorical_crossentropy', optimizer='adam')
        self.model = model
        return model

    def reshape_image(self, image):
        # save the image from the request
        image_path = 'static/img/cache/' + str(uuid.uuid4()) + '.png'
        image.save(image_path)

        # up or downsize the image, whichever is needed
        old_im = Image.open(image_path)
        old_size = old_im.size

        if old_size > (299, 299):
            cover = resizeimage.resize_cover(old_im, [299, 299])
            cover.save(image_path, old_im.format)
        else:
            new_size = (299, 299)
            new_im = Image.new("RGB", new_size)
            new_im.paste(old_im, ((new_size[0]-old_size[0])//2,
                                (new_size[1]-old_size[1])//2))

            new_im.save(image_path)


        # read the image as a numpy array
        image = io.imread(image_path, as_gray=False)
        image = image.reshape(-1, 299, 299, 3)
        image = image.astype('float32')
        image = image / 255

        return image, image_path

    def clear_session(self):
        k.clear_session()
