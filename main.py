import os

import keras.backend as K
import tensorflow as tf
from flask import Blueprint, Flask, g

from controllers.page_controller import page_controller
from controllers.predict_controller import predict_controller
from controllers.rate_controller import rate_controller
from fruit_iris_core.error_handler import ErrorHandler
from helpers.predict_helper import PredictHelper

app = Flask(__name__)

#TODO: move all the following into some some class in fruit_iris_core and call the methods here for this is too messy

# pre-load the helper class / model
app.helper = PredictHelper()
app.helper.load_model('fruit_iris_core/densenet.h5py')
print("MODEL LOADED")

# cleanup cached files
# path = 'static/img/cache/'
# filelist = os.listdir(path)
# for f in filelist:
#     os.remove(os.path.join(path, f))
#     print("FILE '" + path + f + "' DESTROYED")

# print("FILECACHE: EMPTY")

# register the blueprints
# TODO: find some dynamic way to do this
app.register_blueprint(page_controller, url_prefix="/")
app.register_blueprint(predict_controller, url_prefix="/predict")
app.register_blueprint(rate_controller, url_prefix='/rate')

# TODO: a dynamic error handler
@app.errorhandler(404)
def page_not_found(e):
    return ErrorHandler().page_not_found(e)

print("SERVER STARTED")
