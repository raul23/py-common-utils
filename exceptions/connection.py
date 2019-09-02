"""Module that defines exceptions related to connection problems.

These are the exceptions that are raised when querying a server for a resource.

"""


class HTTP404Error(Exception):
    """Raised if the server returns a 404 status code because the page is
    not found."""
    

class WebPageNotFoundError(Exception):
    """Raised if the webpage HTML could not be retrieved for any reasons,
    e.g. 404 error, or OSError."""
