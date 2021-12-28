from interfaces.validator import ValidatorInterface


class LoginValidator(ValidatorInterface):
    username: str
    password: str
