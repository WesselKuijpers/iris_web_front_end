import os

import keras.backend as K
import tensorflow as tf
from flask import Flask

from iris_core.error_handler import errors
from helpers.predict_helper import PredictHelper


# class containing methods for starting the FLASK webserver
# all methods are called in order by calling the start() method
class Server:
    def __init__(self):
        # specify directory for template and static files
        template_dir = os.path.abspath('templates')
        static_dir = os.path.abspath('static')

        # initiate the app
        self.app = Flask(__name__, template_folder=template_dir,
                         static_folder=static_dir)

    # method for calling all methods to start the FLASK webserver
    # returns: VOID
    def start(self):
        # configuring the Tensorflow option to consume only a limited amount of GPU memory
        # pass it to keras as the current session
        # this is done to prevent OOM errors
        gpu_options = tf.GPUOptions(
            per_process_gpu_memory_fraction=0.1, allow_growth=True)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        K.set_session(sess)

        # pipeline for calling all methods
        try:
            self.load_helper()
            self.clean_cache()
            self.register_error_handlers()
            print("SERVER: STARTED")
            return self.app
        except:
            raise

    # method for loading the PredictHelper() class into the application context
    # then load the model into the application context's helper 
    # this model can be used all across the web-app so that the model does not need to be loaded at every request
    # returns: BOOL
    def load_helper(self):
        # instantiate the predicthelper class
        self.app.helper = PredictHelper()

        # load the model
        self.app.helper.load_model('iris_core/models/mobilenet.h5py')

        # if the model is loaded, let the sun shine, else let the user know an error occured
        if(self.app.helper.model):
            print("MODEL: LOADED")
            return True
        else:
            # TODO: throw actual (custom?) error
            print("ERROR: MODEL COULD NOT BE LOADED")
            return False

    # method for cleaning the images in the 'static/image/chache' folder
    # this only happens to images that were not transferred to the respective dataset directory
    # returns: BOOL
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

    # method for registering the error handlers in the 'iris_core/error_handler.py' file
    # returns: VOID
    def register_error_handlers(self):
        # register the error handler
        self.app.register_blueprint(errors)
