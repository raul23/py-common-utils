"""Module that defines exceptions related to files problems.

These are all the exceptions that are raised when reading or writing files.

"""


class OverwriteFileError(Exception):
    """Raised when an existing file is being overwritten."""


class WebPageSavingError(Exception):
    """Raised when the webpage HTML couldn't be saved locally, e.g. the caching
    option is disabled."""
