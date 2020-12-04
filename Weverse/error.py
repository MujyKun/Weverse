class InvalidToken(Exception):
    """Invalid Token was Supplied."""
    def __init__(self):
        super(InvalidToken, self).__init__("An Invalid Bearer Token was Supplied to Weverse.")


class PageNotFound(Exception):
    """Page was not found."""
    def __init__(self, url):
        super(PageNotFound, self).__init__(url + "was an invalid link.")


class BeingRateLimited(Exception):
    """Weverse is rate-limiting. (This issue has not occurred yet)"""
    def __init__(self):
        super(BeingRateLimited, self).__init__("Weverse is rate-limiting the requests.")

