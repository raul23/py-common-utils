"""Module that defines exceptions related to files problems.

These are the exceptions that are raised when reading or writing files.

"""


class OverwriteFileError(Exception):
    """Raised if an existing file is being overwritten."""


class FileReadError(Exception):
    """Raised if the file could not be read from disk, e.g. OSError when the
    file doesn't exist."""


class FileSavingError(Exception):
    """Raised if the webpage HTML couldn't be saved locally, e.g. the caching
    option is disabled."""
