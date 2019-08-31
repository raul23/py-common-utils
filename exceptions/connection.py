"""Module summary

Extended module summary

"""


class HTTP404Error(Exception):
    """Raised if the server returns a 404 status code because the page is
    not found."""
    

class WebPageNotFoundError(Exception):
    """Raised if the webpage HTML could not be retrieved for any reasons,
    e.g. 404 error, or OSError."""
