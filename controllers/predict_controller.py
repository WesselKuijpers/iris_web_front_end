from flask import Blueprint, Flask, abort
from flask import current_app as app
from flask import jsonify, render_template, request
import shutil
import os
import numpy as np

from helpers import predict_helper

predict_controller = Blueprint('predict_controller', __name__)

# TODO: find some better way to do this
classes = [
    'Apple, Black Rot',
    'Apple, Cedar Rust',
    'Apple, Healthy',
    'Apple, Scab',
    'Bell Pepper, Bacterial Spot',
    'Bell Pepper, Healthy',
    'Blueberry, Healthy',
    'Cherry, Healthy',
    'Cherry, Powdery Mildew',
    'Grape, Black Rot',
    'Grape, Esca',
    'Grape, Healthy',
    'Grape, Leaf Blight',
    'Maize, Cercospora Leaf Spot',
    'Maize, Common Rust',
    'Maize, Healthy',
    'Maize, Northern Blight',
    'Orange, Citrus Greening',
    'Peach, Bacterial Spot',
    'Peach, Healthy',
    'Potato, Early Blight',
    'Potato, Healthy',
    'Potato, Late Blight',
    'Raspberry, Healthy',
    'Soybean, Healthy',
    'Squash, Powdery mildew',
    'Strawberry, Healthy',
    'Strawberry, Leaf Scorch',
    'Tomato, Bacterial Spot',
    'Tomato, Early Blight',
    'Tomato, Healthy'
    'Tomato, Late Blight',
    'Tomato, Leaf Mold',
    'Tomato, Mosaic Virus',
    'Tomato, Septoria Leaf Spot',
    'Tomato, Spider Mites',
    'Tomato, Target Spot',
    'Tomato, Yellow Leaf Curl Virus',
]



@predict_controller.route('/', methods=['POST'])
def predict_index():
    try:
        helper = predict_helper.PredictHelper()

        # get the actual model from the running application
        model = app.helper.model

        # get and reshape the image from the form data
        image = request.files['image']
        image = helper.reshape_image(image)

        # make a prediction and make a collection for every item in it
        with app.helper.graph.as_default():
            raw_prediction = np.argmax(model.predict(image[0], batch_size=32, verbose=True))

        return jsonify(classes[raw_prediction], image[1])
    except FileNotFoundError:
        abort(404)
    except ValueError:
        abort(500)
    except:
        abort(503)

@predict_controller.route('/classes')
def get_classes():
    return jsonify(classes)

@predict_controller.route('/save', methods=['POST'])
def predict_save():
    absolute_category = request.form['category'].replace(',', '').replace(' ', '_').lower()
    name = request.form['location'].replace('static/img/cache/', '')
    path = 'dataset/' + absolute_category + '/' + name
    
    os.rename(request.form['location'], path)

    return jsonify({path: path})