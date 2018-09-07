from stargate.helper import http_code


# Error handler
class LanguageError(Exception):
    """
        This is for language error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_400_BAD_REQUEST
