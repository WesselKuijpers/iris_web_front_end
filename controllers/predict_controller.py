from flask import Flask, Blueprint, request, jsonify
from flask import render_template
from helpers import predict_helper
from flask import abort

predict_controller = Blueprint('predict_controller', __name__)

classes = [
    'Cox',
    'Elstar',
    'Golden Delicious',
    'Granny Smith',
    'Nashi Pear',
    'Pink Lady'
]

@predict_controller.route('/', methods=['POST'])
def page_index():
    try:
        helper = predict_helper.PredictHelper()
        # clear the Keras session
        helper.clear_session()
        
        # get the actual model from the local storage by the location in the model object
        model = helper.load_model('iris_core/densenet.h5py')
        
        # get and reshape the image from the form data
        image = request.files['image']
        image = helper.reshape_image(image)

        # make a prediction and make a collection for every item in it
        raw_prediction = model.predict_classes(image)

        # clear the Keras session
        helper.clear_session()

        return jsonify(classes[raw_prediction[0]])
    except FileNotFoundError:
        abort(404)
    except ValueError:
        abort(500)
    except:
        abort(503)
        