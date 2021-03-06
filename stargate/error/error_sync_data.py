from stargate.helper import http_code


# Error handler
class SyncDataError(Exception):
    """
        This is for sync data error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'warning'
        self.status_code = http_code.HTTP_400_BAD_REQUEST
