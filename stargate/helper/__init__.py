import http_code
from stargate.error.error_general import GeneralError


def load_extensions(app):
    """
    To load navitaire extension
    :param app:
    :param name:
    :return:
    """
    if 'stargate' not in app.extensions:
        raise GeneralError({
            "code": "General Error",
            "description": "{name} not exist".format(name='stargate')
        }, 'info', http_code.HTTP_428_PRECONDITION_REQUIRED)

    return app.extensions['stargate']
