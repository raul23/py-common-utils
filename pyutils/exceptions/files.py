"""Module that defines exceptions related to files problems.

These are the exceptions that are raised when reading or writing files.

"""


class OverwriteFileError(Exception):
    """Raised if an existing file is being overwritten and the flag to
    overwrite files is disabled."""
