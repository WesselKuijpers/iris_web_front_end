from controllers.page_controller import page_controller
from controllers.predict_controller import predict_controller
from controllers.rate_controller import rate_controller
from controllers.translate_controller import translate_controller
from controllers.insight_controller import insight_controller

class Router:
    def register(self):
        # import the app context, is done locally so that an importerror is not raised
        from main import app

        # register all the required functional blueprints pointing to the controllers
        app.register_blueprint(page_controller, url_prefix="/")
        app.register_blueprint(predict_controller, url_prefix="/predict")
        app.register_blueprint(rate_controller, url_prefix='/rate')
        app.register_blueprint(translate_controller, url_prefix='/translate')
        app.register_blueprint(insight_controller, url_prefix='/insight')
