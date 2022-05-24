from flask import Flask

from app.main.api import handle_bad_request
from app.main.api.pagila import pagila_api
from app.main.config import Configuration

app = Flask(__name__)
Configuration.load()
config = Configuration()

if __name__ == '__main__':
    app.register_blueprint(pagila_api, url_prefix='/api')
    app.register_error_handler(500, handle_bad_request)
    app.run(host='0.0.0.0')
