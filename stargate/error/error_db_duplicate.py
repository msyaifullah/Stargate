from stargate.helper import http_code


# Error handler
class DBDuplicateError(Exception):
    """
        This is for db duplicate error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'warning'
        self.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
