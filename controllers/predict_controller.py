from flask import Blueprint, Flask, abort
from flask import current_app as app
from flask import jsonify, render_template, request
import shutil
import os

from helpers import predict_helper

predict_controller = Blueprint('predict_controller', __name__)

# TODO: find some better way to do this
classes = [
    'Cox',
    'Elstar',
    'Golden Delicious',
    'Granny Smith',
    'Nashi Pear',
    'Pink Lady'
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
            raw_prediction = model.predict_classes(image[0], verbose=True)

        return jsonify(classes[raw_prediction[0]], image[1])
    except FileNotFoundError:
        abort(404)
    except ValueError:
        abort(500)
    except:
        abort(503)

@predict_controller.route('/save', methods=['POST'])
def predict_save():
    absolute_category = request.form['category'].replace(' ', '_').lower()
    name = request.form['location'].replace('static/img/cache/', '')
    train_path = 'dataset/train/' + absolute_category + '/'
    test_path = 'dataset/test/' + absolute_category + '/'

    if (len(os.listdir(train_path)) >= 10 and len(os.listdir(train_path)) % 10 == 0):
        path = test_path + name
    else:
        path = train_path + name
    
    os.rename(request.form['location'], path)

    return jsonify({path: path})