from flask import Blueprint, Flask, redirect, url_for
import config, os

from cStringIO import StringIO

class WSGIRawBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['raw'] = body
        environ['wsgi.input'] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback



app = Flask(__name__, static_url_path=config.APPLICATION_ROOT+'/static')
bp = Blueprint(config.APPLICATION_ROOT, __name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = WSGIRawBody(ProxyFix(app.wsgi_app))

app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))

app.config.APPLICATION_ROOT=config.APPLICATION_ROOT
app.config.PREFERRED_URL_SCHEME=config.PREFERRED_URL_SCHEME
app.config.AUTH_COOKIE_NAME=config.AUTH_COOKIE_NAME
app.config.AUTH_REDIRECT=config.AUTH_REDIRECT
app.config.AUTH_SECRET=config.AUTH_SECRET

# Always log
import logging
file_handler = logging.FileHandler(config.LOGFILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

from filters import *
app.jinja_env.filters['status_class'] = status_class
app.jinja_env.filters['friendly_time'] = friendly_time
app.jinja_env.filters['friendly_size'] = friendly_size
app.jinja_env.filters['to_qs'] = to_qs
app.jinja_env.filters['approximate_time'] = approximate_time
app.jinja_env.filters['exact_time'] = exact_time
app.jinja_env.filters['short_date'] = short_date

# app.add_url_rule('/robots.txt', redirect_to=url_for('static', filename='robots.txt'))

from requestbin import api, views
app.register_blueprint(bp, url_prefix=config.APPLICATION_ROOT)
logging.info("App prefix="+config.APPLICATION_ROOT)
