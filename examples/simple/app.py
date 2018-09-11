from flask import Flask
from flask import jsonify
from flask import request

from stargate.base import Startgate
from stargate.helper import http_code
from stargate.decorator_auth import requires_auth
from stargate.decorator_auth import requires_bearer_auth
from stargate.decorator_auth import requires_refresh_auth
from stargate.decorator_auth import requires_device

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['FLASK_ENV'] = 'development'


# Flask views
@app.route('/')
def index():
    return jsonify({
        'status': 'OK',
        'environment': app.config.get('FLASK_ENV')
    }), http_code.HTTP_200_OK


@app.route("/tests", methods=['POST'])
@requires_device
@requires_auth
def get_test_auth(**kwargs):
    print(kwargs['payload'])

    start_gate = Startgate()
    token_access_payload, token_access = start_gate.encode_auth_token(secret='123456', user_id='12345', sender_id='sender-1234',
                                                                      recipients_id='recipients-1234')
    token_refresh_payload, token_refresh = start_gate.encode_refresh_token(secret='123456', user_id='12345', sender_id='sender-1234',
                                                                           recipients_id='recipients-1234')
    return jsonify(
        message="i got this user",
        token_access_payload=token_access_payload,
        token_access=token_access,
        token_refresh_payload=token_refresh_payload,
        token_refresh=token_refresh,
    ), http_code.HTTP_202_ACCEPTED


@app.route("/test/bearer/<client_id>", methods=['POST'])
@requires_bearer_auth
def get_test_bearer(client_id, **kwargs):
    print(client_id)
    print(kwargs['jwt_payload'])

    return jsonify(
        message="this is test bearer with id " + client_id,
        data=kwargs.get('jwt_payload')
    ), http_code.HTTP_200_OK


@app.route("/test/refresh/<client_id>", methods=['POST'])
@requires_refresh_auth
def get_test_refresh(client_id, **kwargs):
    print(client_id)
    print(kwargs['jwt_payload'])

    return jsonify(
        message="this is test refresh with id " + client_id,
        data=kwargs.get('jwt_payload')
    ), http_code.HTTP_200_OK


if __name__ == '__main__':
    # Start app
    app.run(debug=True)
