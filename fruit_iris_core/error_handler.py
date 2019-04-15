from flask import render_template


class ErrorHandler:
    def page_not_found(self, e):
        return render_template('errors/404.html'), 404
