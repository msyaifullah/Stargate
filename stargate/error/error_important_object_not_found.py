from stargate.helper import http_code


# Error handler
class ImportantObjectNotFoundError(Exception):
    """
        This is for important object error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'warning'
        self.status_code = http_code.HTTP_404_NOT_FOUND
