import os
import logging
import datetime
import functools
import jwt

from flask import Flask, jsonify, request, abort

# Ensure environment variables are loaded
JWT_SECRET = os.getenv('JWT_SECRET', 'abc123abc1234')  # Default value is provided in case it's missing
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Configure logger
def _logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log

LOG = _logger()
LOG.debug("Starting with log level: %s" % LOG_LEVEL )
APP = Flask(__name__)

def require_jwt(function):
    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except:
            abort(401)

        return function(*args, **kws)
    return decorated_function


# Route handlers
@APP.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Healthy")

@APP.route('/auth', methods=['POST'])
def auth():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        LOG.error("No email provided")
        return jsonify({"message": "Missing parameter: email"}), 400
    if not password:
        LOG.error("No password provided")
        return jsonify({"message": "Missing parameter: password"}), 400
    user_data = {'email': email, 'password': password}
    token = _get_jwt(user_data).decode('utf-8')
    return jsonify(token=token)

@APP.route('/contents', methods=['GET'])
def decode_jwt():
    if not 'Authorization' in request.headers:
        abort(401)
    data = request.headers['Authorization']
    print("Authorization header:", data)  # Debugging line
    token = str.replace(str(data), 'Bearer ', '')
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        print("Decoded data:", data)  # Debugging line
    except Exception as e:
        print("JWT decode error:", e)  # Debugging line
        abort(401)

    response = {'email': data['email'], 'exp': data['exp'], 'nbf': data['nbf']}
    return jsonify(**response)


# Helper function to create JWT token
def _get_jwt(user_data):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {'exp': exp_time, 'nbf': datetime.datetime.utcnow(), 'email': user_data['email']}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=3000)
