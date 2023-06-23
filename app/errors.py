class UserNotFoundException(Exception):
    """When the given user was not found"""


class PasswordNotMatchedException(Exception):
    """When the password not match"""


class DBError(Exception):
    """When there's a problem in DB"""


class CorruptedTokenError(Exception):
    """When there is a problem to decode a token"""


class EmptyDataError(Exception):
    """When decode data not return anything"""


class InactiveUserError(Exception):
    """When decode data not return anything"""


class RuleRelatedToResultError(Exception):
    """When decode data not return anything"""
