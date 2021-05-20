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

