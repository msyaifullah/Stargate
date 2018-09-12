import logging
from flask import jsonify

from stargate.helper import http_code

from .error_auth import AuthError
from .error_general import GeneralError
from .error_db_corrupt import DBCorruptError
from .error_db_duplicate import DBDuplicateError
from .error_device import DeviceError
from .error_empty_data import EmptyDataError
from .error_forbidden import ForbiddenError
from .error_important_object_not_found import ImportantObjectNotFoundError
from .error_insufficient_requirements import InsufficientRequirementsError
from .error_internal_parse import InternalParseError
from .error_invalid_auth import InvalidAuthError
from .error_invalid_body import InvalidBodyError
from .error_invalid_header import InvalidHeaderError
from .error_invalid_param import InvalidParamError
from .error_invalid_query import InvalidQueryError
from .error_language import LanguageError
from .error_location import LocationError
from .error_missing_auth import MissingAuthError
from .error_missing_body import MissingBodyError
from .error_missing_header import MissingHeaderError
from .error_missing_param import MissingParamError
from .error_missing_query import MissingQueryError
from .error_object_expired import ObjectExpiredError
from .error_object_inactive import ObjectInactiveError
from .error_object_not_found import ObjectNotFoundError
from .error_resource_unavailable import ResourceUnavailableError
from .error_server_auth import ServerAuthError
from .error_sync_data import SyncDataError
from .error_timestamp import TimestampError
from .error_user_inactive import UserInactiveError
from .error_verification import VerificationError

__all__ = ['register_errors']


def register_errors(app):
    """
    register errors module
    """

    @app.errorhandler(500)
    def internal_server(ex):
        logging.exception('The server encountered an internal error')
        response = jsonify(status="error", severity='error', message="The server encountered an internal error and was "
                                                                     "unable to complete your request. "
                                                                     "Either the server is overloaded or there is an "
                                                                     "error in the application.")
        response.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
        return response

    @app.errorhandler(404)
    def page_not_found(ex):
        logging.exception('An error occurred during a request. page not found')
        response = jsonify(status="error", severity='error', message="page not found")
        response.status_code = http_code.HTTP_404_NOT_FOUND
        return response

    @app.errorhandler(GeneralError)
    @app.errorhandler(AuthError)
    @app.errorhandler(DBCorruptError)
    @app.errorhandler(DBDuplicateError)
    @app.errorhandler(DeviceError)
    @app.errorhandler(EmptyDataError)
    @app.errorhandler(ForbiddenError)
    @app.errorhandler(ImportantObjectNotFoundError)
    @app.errorhandler(InsufficientRequirementsError)
    @app.errorhandler(InternalParseError)
    @app.errorhandler(InvalidAuthError)
    @app.errorhandler(InvalidBodyError)
    @app.errorhandler(InvalidHeaderError)
    @app.errorhandler(InvalidParamError)
    @app.errorhandler(InvalidQueryError)
    @app.errorhandler(LanguageError)
    @app.errorhandler(LocationError)
    @app.errorhandler(MissingAuthError)
    @app.errorhandler(MissingBodyError)
    @app.errorhandler(MissingHeaderError)
    @app.errorhandler(MissingParamError)
    @app.errorhandler(MissingQueryError)
    @app.errorhandler(ObjectExpiredError)
    @app.errorhandler(ObjectInactiveError)
    @app.errorhandler(ObjectNotFoundError)
    @app.errorhandler(ResourceUnavailableError)
    @app.errorhandler(ServerAuthError)
    @app.errorhandler(SyncDataError)
    @app.errorhandler(TimestampError)
    @app.errorhandler(UserInactiveError)
    @app.errorhandler(VerificationError)
    def handle_all_error(ex):
        # Log the error and stacktrace.
        logging.exception('An error occurred during a request.')
        response = jsonify(status="error", severity=ex.severity, message=ex.error)
        response.status_code = ex.status_code
        return response
    # [END error handles]
