from flask import Flask, Blueprint, request
from controllers.page_controller import page_controller
# from controllers.predict_controller import predict_controller
from helpers.predict_helper import PredictHelper
from flask import g
from controllers.predict_controller import PredictController
import tensorflow as tf
import keras.backend as K

app = Flask(__name__)

global graph
graph = tf.get_default_graph()
model = PredictHelper().load_model('iris_core/densenet.h5py')
print("LOADING: DONE")

app.register_blueprint(page_controller, url_prefix="/")
# app.register_blueprint(predict_controller, url_prefix="/predict")

@app.route('/predict/', methods=['POST'])
def predict():
    controller = PredictController()
    result = controller.predict_index(request, model, graph)
    return result
