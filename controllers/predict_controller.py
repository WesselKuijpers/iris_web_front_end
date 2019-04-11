from flask import Flask, Blueprint, jsonify
from flask import render_template
from helpers import predict_helper
from flask import abort
from flask import current_app as app
import tensorflow as tf
import keras.backend as K

predict_controller = Blueprint('predict_controller', __name__)

class PredictController:
    def __init__(self):
        # TODO: make this dynamic
        self.classes = [
            'Cox',
            'Elstar',
            'Golden Delicious',
            'Granny Smith',
            'Nashi Pear',
            'Pink Lady'
        ]

    # @predict_controller.route('/', methods=['POST'])
    def predict_index(self, request, model, graph):
        try:
            helper = predict_helper.PredictHelper()

            # get the actual model from the local storage by the location in the model object
            # model = helper.load_model('iris_core/densenet.h5py')

            # get and reshape the image from the form data
            image = request.files['image']
            image = helper.reshape_image(image)

            # make a prediction and make a collection for every item in it
            with graph.as_default():
                raw_prediction = model.predict_classes(image[0])

            return jsonify(self.classes[raw_prediction[0]], image[1])
        except FileNotFoundError:
            # abort(404)
            raise
        except ValueError:
            raise
            # abort(500)
        except:
            raise
            # abort(503)
        