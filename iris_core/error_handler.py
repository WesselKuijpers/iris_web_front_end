from flask import render_template, Blueprint

# register blueprint
errors = Blueprint('errors', __name__)


# method for catching 404 (not found) errors
# returns: 'templates/errors/404.html' template
@errors.app_errorhandler(404)
def page_not_found(self):
    return render_template('errors/404.html')
