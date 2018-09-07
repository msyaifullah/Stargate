from stargate.helper import http_code


# Error handler
class EmptyDataError(Exception):
    """
        This is for empty data error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'error'
        self.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
