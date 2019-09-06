"""Module that defines exceptions related to connection problems.

These are the exceptions that are raised when querying a server for a resource.

"""


class HTTP404Error(Exception):
    """Raised if the server returns a 404 status code because the webpage is
    not found."""
    

class WebPageNotFoundError(Exception):
    """Raised if the webpage HTML could not be retrieved because of any
    connection problems, e.g. 404 error."""
