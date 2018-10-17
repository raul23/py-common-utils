# TODO: only `OverwriteFileError` should be here
class EmptyQueryResultSetError(Exception):
    """Raised when a SQL query returns an empty result set, i.e. no rows."""


class HTTP404Error(Exception):
    """Raised when the server returns a 404 status code because the page is
    not found."""


class OverwriteFileError(Exception):
    """Raised when an existing file is being overwritten."""


class WebPageNotFoundError(Exception):
    """Raised when the webpage HTML could not be retrieved for any reasons,
    e.g. 404 error, or OSError."""


class WebPageSavingError(Exception):
    """Raised when the webpage HTML couldn't be saved locally, e.g. the caching
    option is disabled."""
