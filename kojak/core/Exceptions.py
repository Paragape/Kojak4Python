"""
Created on February 10, 2017

@author: John Jackson
"""


class KojakException(Exception):
    """
    This is the base exception for all exceptions that Kojak throws.
    """

    def __init__(self, message: str):
        """
        Create a Kojak exception.
        @param message: The message describing the exception.
        """

        self._message = message

    def __str__(self):
        return self.__class__.__name__ + ': ' + self._message


class AbortException(KojakException):
    """
    Throw this exception when a catastrophic error occurs and the test should be terminated.
    """
    pass


class HardException(KojakException):
    """
    Throw this exception when an error occurs that is significant enough to abort the scenario.
    """
    pass


class SoftException(KojakException):
    """
    Throw this exception when a verification fails that is not significant enough to abort the scenario.
    """
    pass
