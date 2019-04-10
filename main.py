from flask import Flask, Blueprint, request
from controllers.page_controller import page_controller
# from controllers.predict_controller import predict_controller
from helpers.predict_helper import PredictHelper
from flask import g
from controllers.predict_controller import PredictController

app = Flask(__name__)

PredictHelper().clear_session()
model = PredictHelper().load_model('iris_core/densenet.h5py')
print("LOADING: DONE")

app.register_blueprint(page_controller, url_prefix="/")
# app.register_blueprint(predict_controller, url_prefix="/predict")

@app.route('/predict/', methods=['POST'])
def predict():
    PredictHelper().clear_session()
    controller = PredictController()
    result = controller.predict_index(request, model)
    return result

PredictHelper().clear_session()
