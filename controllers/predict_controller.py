from flask import Flask, Blueprint, jsonify
from flask import render_template
from helpers import predict_helper
from flask import abort
from flask import current_app as app

predict_controller = Blueprint('predict_controller', __name__)

class PredictController:
    def __init__(self):
        # TODO: find some better way to do this, it annoyes me...
        self.classes = [
            'Cox',
            'Elstar',
            'Golden Delicious',
            'Granny Smith',
            'Nashi Pear',
            'Pink Lady'
        ]

    # @predict_controller.route('/', methods=['POST'])
    def predict_index(self, request, model):
        try:
            helper = predict_helper.PredictHelper()
            # clear the Keras session
            helper.clear_session()

            # get the actual model from the local storage by the location in the model object
            # model = helper.load_model('iris_core/densenet.h5py')
            model = model

            # get and reshape the image from the form data
            image = request.files['image']
            image = helper.reshape_image(image)

            # make a prediction and make a collection for every item in it
            raw_prediction = model.predict_classes(image[0])

            # clear the Keras session
            helper.clear_session()

            return jsonify(self.classes[raw_prediction[0]], image[1])
        except FileNotFoundError:
            # abort(404)
            raise
        except ValueError:
            raise
            # abort(500)
        except:
            # raise
            abort(503)
        