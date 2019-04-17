import os

import keras.backend as K
import tensorflow as tf
from flask import Blueprint, Flask, g

from controllers.page_controller import page_controller
from controllers.predict_controller import predict_controller
from controllers.rate_controller import rate_controller
from fruit_iris_core.error_handler import errors
from helpers.predict_helper import PredictHelper


class Server:
    def __init__(self):
        template_dir = os.path.abspath('templates')
        static_dir = os.path.abspath('static')
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    def boot(self):
        try:
            self.load_helper()
            self.clean_cache()
            self.register_blueprints()
            self.register_error_handlers()
            print("SERVER: STARTED")
            return self.app
        except:
            print("AN ERROR OCCURED")
            raise

    def load_helper(self):
        self.app.helper = PredictHelper()
        self.app.helper.load_model('fruit_iris_core/densenet.h5py')
        if(self.app.helper.model):
            print("MODEL: LOADED")
            return True
        else:
            # TODO: throw actual (custom?) error
            print("ERROR: MODEL COULD NOT BE LOADED")
            return False

    def clean_cache(self):
        path = 'static/img/cache/'
        filelist = os.listdir(path)
        for f in filelist:
            os.remove(os.path.join(path, f))
            print("FILE '" + path + f + "' DESTROYED")
        if(len(filelist) == 0):
            print("FILECACHE: CLEAN")
            return True
        else:
            # TODO: throw actual (custom?) error
            print("ERROR: FILECACHE COULD NOT BE CLEANED")
            return False
        
    def register_blueprints(self):
        # TODO: find some dynamic way to do this
        self.app.register_blueprint(page_controller, url_prefix="/")
        self.app.register_blueprint(predict_controller, url_prefix="/predict")
        self.app.register_blueprint(rate_controller, url_prefix='/rate')

    def register_error_handlers(self):
        # TODO: find some dynamic way to do this
        self.app.register_blueprint(errors)
