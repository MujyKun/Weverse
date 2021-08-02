class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""
    def __init__(self):
        super(InvalidToken, self).__init__("An Invalid Bearer Token was Supplied to Weverse.")


class PageNotFound(Exception):
    r"""
    An Exception Raised When a link was not found.

    Parameters
    ----------
    url: :class:`str`
        The link that was not found.
    """
    def __init__(self, url):
        super(PageNotFound, self).__init__(url + "was an invalid link.")


class BeingRateLimited(Exception):
    """An Exception Raised When Weverse Is Being Rate-Limited."""
    def __init__(self):
        super(BeingRateLimited, self).__init__("Weverse is rate-limiting the requests.")


class LoginFailed(Exception):
    """An Exception raised when the login failed."""
    def __init__(self, msg: str = "The login process for Weverse had failed."):
        super(LoginFailed, self).__init__(msg)


class InvalidCredentials(Exception):
    """An Exception raised when no valid credentials were supplied."""
    def __init__(self, msg: str = "The credentials for a token or a username/password could not be found."):
        super(InvalidCredentials, self).__init__(msg)


class NoHookFound(Exception):
    """An Exception raised when a loop for the hook was started but did not actually have a hook method."""
    def __init__(self, msg: str = "No Hook was passed into the Weverse client."):
        super(NoHookFound, self).__init__(msg)
