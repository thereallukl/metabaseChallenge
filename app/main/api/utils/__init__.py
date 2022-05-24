from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app.main.config import Configuration


auth = HTTPBasicAuth()

config = Configuration()
api_auth = {
    "api": generate_password_hash(config.api_auth_password)
}


@auth.verify_password
def verify_password(username, password):
    if username in api_auth and \
            check_password_hash(api_auth.get(username), password):
        return username