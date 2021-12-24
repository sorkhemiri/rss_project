GENERAL_ERROR = 1
VALIDATION_ERROR = 2
AUTHORIZATION_ERROR = 3
DOES_NOT_EXIST_ERROR = 4
LOGICAL_ERROR = 5
CONNECTION_ERROR = 6


class GeneralError:
    error_code = 1
    message = "GENERAL ERROR"
    status_code = 400


class ValidationError:
    error_code = 2
    message = "VALIDATION ERROR"
    status_code = 400


class AuthorizationError:
    error_code = 3
    message = "AUTHORIZATION ERROR"
    status_code = 401


class DoesNotExistError:
    error_code = 4
    message = "DOES NOT EXIST ERROR"
    status_code = 404


class LogicalError:
    error_code = 5
    message = "LOGICAL ERROR"
    status_code = 400


class ConnectingError:
    error_code = 6
    message = "CONNECTING ERROR"
    status_code = 400
