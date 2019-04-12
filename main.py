import keras.backend as K
import tensorflow as tf
from flask import Blueprint, Flask, g

from controllers.page_controller import page_controller
from controllers.predict_controller import predict_controller
from helpers.predict_helper import PredictHelper

import os

app = Flask(__name__)

# pre-load the helper class / model
app.helper = PredictHelper()
app.helper.load_model('iris_core/densenet.h5py')
print("LOADING: DONE")

# cleanup cached files
path = 'static/img/cache/'
filelist = os.listdir(path)
for f in filelist:
    os.remove(os.path.join(path, f))

# register the blueprints
# TODO: find some dynamic way to do this
app.register_blueprint(page_controller, url_prefix="/")
app.register_blueprint(predict_controller, url_prefix="/predict")
