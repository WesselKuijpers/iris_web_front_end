import json
import os

import numpy as np
from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, render_template, request

from helpers import predict_helper

# register blueprint
predict_controller = Blueprint('predict_controller', __name__)


# route: '/predict/'
# returns: a string representing the predicted class (based on the POST data) and the path to the cached image
# method: POST
@predict_controller.route('/', methods=['POST'])
def predict_index():
    with open('iris_core/classes.json', 'r') as file:
        classes = json.load(file)

    try:
        helper = predict_helper.PredictHelper()

        # get the actual model from the running application
        model = app.helper.model

        # get and reshape the image from the form data
        image = request.files['image']
        image = helper.reshape_image(image)

        # make a prediction and make a collection for every item in it
        with app.helper.graph.as_default():
            raw_prediction = np.argmax(model.predict(
                image[0], batch_size=32, verbose=True))

        return jsonify(classes[raw_prediction], image[1])
    except FileNotFoundError:
        abort(404)
    except ValueError:
        abort(500)
    except:
        abort(503)

# route: '/predict/classes'
# returns: json response containing the dataset classes read from the 'iris_core/classes.json' -file
@predict_controller.route('/classes')
def get_classes():
    with open('iris_core/classes.json', 'r') as file:
        classes = json.load(file)
    return jsonify(classes)

# route: '/predict/save'
# returns: returns the path to the image that was saved from the post data
# method: POST
@predict_controller.route('/save', methods=['POST'])
def predict_save():
    absolute_category = request.form['category'].replace(
        ',', '').replace(' ', '_').lower()
    name = request.form['location'].replace('static/img/cache/', '')
    path = 'dataset/train' + absolute_category + '/' + name

    os.rename(request.form['location'], path)

    return jsonify({path: path})
