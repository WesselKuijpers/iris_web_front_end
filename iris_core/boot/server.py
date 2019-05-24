from flask import Flask
import os

from iris_core.error_handler import errors


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
        
        # pipeline for calling all methods
        try:
            self.register_error_handlers()
            print("SERVER: STARTED")
            return self.app
        except:
            raise

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
