import os

import keras.backend as K
import tensorflow as tf
from flask import Blueprint, Flask, g

import controllers

from fruit_iris_core.error_handler import errors
from helpers.predict_helper import PredictHelper


class Server:
    def __init__(self):
        # specify directory for template and static files
        template_dir = os.path.abspath('templates')
        static_dir = os.path.abspath('static')

        # initiate the app
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    def start(self):
        # pipeline for calling all methods
        try:
            self.load_helper()
            self.clean_cache()
            self.register_error_handlers()
            print("SERVER: STARTED")
            return self.app
        except:
            print("AN ERROR OCCURED")
            raise

    def load_helper(self):
        # instantiate the predicthelper class
        self.app.helper = PredictHelper()
        # load the model
        self.app.helper.load_model('fruit_iris_core/models/mobilenet.h5py')

        # if the model is loaded, let the sun shine, else let the user know an error occured
        if(self.app.helper.model):
            print("MODEL: LOADED")
            return True
        else:
            # TODO: throw actual (custom?) error
            print("ERROR: MODEL COULD NOT BE LOADED")
            return False

    def clean_cache(self):
        # clean all the images that were saved for prediction purposes
        path = 'static/img/cache/'
        filelist = os.listdir(path)
        for f in filelist:
            os.remove(os.path.join(path, f))
            print("FILE '" + path + f + "' DESTROYED")

        # if the clean action is succesfull, continue, else return error
        if(len(filelist) == 0):
            print("FILECACHE: CLEAN")
            return True
        else:
            # TODO: throw actual (custom?) error
            print("ERROR: FILECACHE COULD NOT BE CLEANED")
            return False

    def register_error_handlers(self):
        # register the error handler
        self.app.register_blueprint(errors)
