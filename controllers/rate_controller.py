from flask import Blueprint, render_template

# register blueprint
rate_controller = Blueprint('rate_controller', __name__)


# route: '/rate/'
# returns: renders the 'templates/rate/index.html' template
@rate_controller.route('/')
def rate_index():
    return render_template('rate/index.html')
