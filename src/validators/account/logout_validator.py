from interfaces.validator import ValidatorInterface


class LogoutValidator(ValidatorInterface):
    auth_token: str
