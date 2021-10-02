GENERAL_ERROR = 1
VALIDATION_ERROR = 2
AUTHORIZATION_ERROR = 3
DOES_NOT_EXIST_ERROR = 4
LOGICAL_ERROR = 5
CONNECTION_ERROR = 6


class GeneralError:
    error_code = 1
    message = "general error"


class ValidationError:
    error_code = 2
    message = "validation error"


class AuthorizationError:
    error_code = 3
    message = "authorization error"


class DoesNotExistError:
    error_code = 4
    message = "does not exist error"


class LogicalError:
    error_code = 5
    message = "logical error"


class ConnectingError:
    error_code = 6
    message = "connecting error"
