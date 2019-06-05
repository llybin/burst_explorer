class BurstException(Exception):
    """The base Burst Exception that all other exception classes extend."""


class APIException(BurstException):
    """Indicate exception that involve responses from Burst's API."""


class ClientException(BurstException):
    """Indicate exceptions that don't involve interaction with Burst's API."""
