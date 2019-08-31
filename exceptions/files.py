"""Module summary

Extended module summary

"""


class OverwriteFileError(Exception):
    """Raised when an existing file is being overwritten."""


class WebPageSavingError(Exception):
    """Raised when the webpage HTML couldn't be saved locally, e.g. the caching
    option is disabled."""
