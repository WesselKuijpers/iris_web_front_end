from flask import Flask, Blueprint
from controllers.page_controller import page_controller
from controllers.predict_controller import predict_controller

app = Flask(__name__)

app.register_blueprint(page_controller, url_prefix="/")
app.register_blueprint(predict_controller, url_prefix="/predict")
