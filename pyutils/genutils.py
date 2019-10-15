"""Module that defines many general and useful functions.

You will find such functions as loading a YAML file, writing to a file on disk,
and getting the local time based on the current time zone.

See Also
--------
dbutils : module that defines database-related functions.
logutils : module that defines log-related functions.
saveutils : module that defines a class for saving webpages on disk.


.. _logging_wrapper.py: https://bit.ly/2kofzpo
.. _PermissionError Errno 13 Permission denied (stackoverflow):
   https://stackoverflow.com/a/50759281
.. _PyYAML yaml.load(input) Deprecation: https://msg.pyyaml.org/load
.. _Stack Overflow's user Mark Amery:
   http://stackoverflow.com/a/39501288/1709587
.. _Stack Overflow's user Nick Stinemates:
    https://stackoverflow.com/a/185941

"""

import codecs
from datetime import datetime
import json
import os
import pathlib
import platform
import pickle
import shlex
import shutil
import subprocess


def convert_utctime_to_local_tz(utc_time=None):
    """Convert a given UTC time into the local time zone.

    If a UTC time is given, it is converted to the local time zone. If
    `utc_time` is None, then the current time based on the local time zone is
    returned.

    The date and time are returned as a string with format
    ``YYYY-MM-DD HH:MM:SS-HH:MM``

    The modules :mod:`pytz` and :mod:`tzlocal` need to be installed. You can
    install them with ``pip``::

        $ pip install tzlocal

    This will also install :mod:`pytz`.

    Parameters
    ----------
    utc_time: time.struct_time
        The UTC time to be converted in the local time zone (the default value
        is None which implies that the current time will be retrieved and
        converted into the local time zone).

    Returns
    -------
    local_time: str
        The UTC time converted into the local time zone with the format
        ``YYYY-MM-DD HH:MM:SS-HH:MM``

    Raises
    ------
    ImportError
        Raised if the modules :mod:`tzlocal` and :mod:`pytz` are not found.

    Examples
    --------
    >>> import time
    >>> utc_time = time.gmtime()
    >>> convert_utctime_to_local_tz(utc_time)
    '2019-09-05 18:17:59-04:00'

    """
    try:
        import pytz
        import tzlocal
    except ImportError as e:
        raise ImportError("tzlocal and pytz not found. You can install them "
                          "with: pip install tzlocal. This will also install "
                          "pytz.")
    else:
        # Get the local timezone name
        tz = pytz.timezone(tzlocal.get_localzone().zone)
        if utc_time:
            # Convert time.struct_time into datetime
            # Only the date and time up to seconds, e.g. (2019, 9, 5, 22, 12, 33)
            utc_time = datetime(*utc_time[:6])
            # Convert time zone unaware ``datetime`` object into aware timezone
            # datetime object
            utc_time = utc_time.replace(tzinfo=pytz.UTC)
            # Convert the UTC time into the local time zone
            local_time = utc_time.astimezone(tz)
        else:
            # Get the time in the system's time zone
            local_time = datetime.now(tz)
            # Remove microseconds
            local_time = local_time.replace(microsecond=0)
        # Use date format: YYYY-MM-DD HH:MM:SS-HH:MM
        # ISO format is YYYY-MM-DDTHH:MM:SS-HH:MM
        local_time = local_time.isoformat().replace("T", " ")
        return local_time


def create_dir(dirpath, overwrite=False):
    """Create a directory if it doesn't already exist.

    Parameters
    ----------
    dirpath : str
        Path to the directory to be created.
    overwrite : bool, optional
        TODO: redo tests with overwrite=True

    Returns
    -------
    dirpath: str
        If the directory was successfully created, the path to the directory is
        returned.

    Raises
    ------
    FileExistsError
        Raised if the directory already exists.
    PermissionError
        Raised if trying to run an operation without the adequate access rights
        - for example filesystem permissions (See :exc:`PermissionError`).

        Also, on Windows, the :exc:`PermissionError` can occur if you try to
        open a directory as a file. Though, the error is more accurate in Linux:
        "[Errno 21] Is a directory" (See `PermissionError Errno 13 Permission
        denied (stackoverflow)`_)

    """
    try:
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=overwrite)
    except FileExistsError:
        raise
    except PermissionError:
        raise
    else:
        return dirpath


def create_timestamped_dir(parent_dirpath, suffix=""):
    """Create a timestamped directory if it doesn't already exist.

    The timestamp consists in `YYYYMMDD-HHMMSS` and is added to the beginning
    of the directory name, e.g.::

        /Users/test/20190905-122929-documents

    Parameters
    ----------
    parent_dirpath : str
        Path to the parent directory.

    suffix : str, optional
        It will be added in the directory name after the timestamp (the default
        value is "" which implies that only the timestamp will be added as the
        name of the directory).

    Returns
    -------
    new_dirpath : str
        Path to the newly created directory.

    Raises
    ------
    FileExistsError
        Raised if the directory already exists.
    PermissionError
        Raised if trying to run an operation without the adequate access rights.

    """
    new_dirname = "-{}".format(suffix) if suffix else suffix
    timestamped = datetime.now().strftime('%Y%m%d-%H%M%S{dirname}')
    new_dirpath = os.path.join(
        parent_dirpath, timestamped.format(dirname=new_dirname))
    try:
        pathlib.Path(new_dirpath).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise
    except PermissionError:
        raise
    else:
        return new_dirpath


def delete_folder_contents(folderpath, remove_subdirs=True, delete_recursively=False):
    """Delete the contents of a folder.

    The folder itself won't be removed!

    The code is from `Stack Overflow's user Nick Stinemates`_.

    By default, this function deletes everything in the folder, including
    files and subdirectories. However, if subdirectories must not be deleted,
    then `remove_subdirs` must be set to False.

    IMPORTANT: TODO about deleting recursively

    Parameters
    ----------
    folderpath : str
        Path to the folder whose content will be deleted.
    remove_subdirs : bool, optional
        Remove the subdirectories (the default value is True which implies that
        everything will be deleted from the root folder).
    delete_recursively: bool, optional
        TODO

    Raises
    ------
    OSError
        Raised if any I/O related occurs while writing the data to disk, e.g.
        the file doesn't exist.

    """
    def remove_non_recursively():
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)
            if os.path.isfile(filepath):
                os.unlink(filepath)
            elif remove_subdirs and os.path.isdir(filepath):
                shutil.rmtree(filepath)

    def remove_recursively():
        for root, dirs, files in os.walk(folderpath):
            for f in files:
                os.unlink(os.path.join(root, f))
            if remove_subdirs:
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    try:
        if delete_recursively:
            remove_recursively()
        else:
            remove_non_recursively()
    except OSError:
        raise


def dump_pickle(filepath, data):
    """Write data to a pickle file.

    Parameters
    ----------
    filepath: str
        Path to the pickle file where data will be written.
    data:
        Data to be saved on disk.

    Raises
    ------
    OSError
        Raised if any I/O related occurs while writing the data to disk, e.g.
        the file doesn't exist.

    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    except OSError:
        raise


def dumps_json(filepath, data, encoding='utf8', sort_keys=True,
               ensure_ascii=False):
    """Write data to a JSON file.

    The data is first serialized to a JSON formatted string and then saved
    to disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file where the data will be saved.

    data
        Data to be written to the JSON file.

    encoding : str, optional
        Encoding to be used for opening the JSON file in write mode (the
        default value is 'utf8').

    sort_keys : bool, optional
        If `sort_keys` is true, then the output of dictionaries will be sorted
        by key. See the :meth:`json.dumps` docstring description. (the default
        value is True).

    ensure_ascii : bool, optional
        If `ensure_ascii` is False, then the return value can contain
        non-ASCII characters if they appear in strings contained in `data`.
        Otherwise, all such characters are escaped in JSON strings. See the
        :meth:`json.dumps` docstring description (the default value is False).

    Raises
    ------
    OSError
        Raised if any I/O related occurs while writing the data to disk, e.g.
        the file doesn't exist.

    """
    try:
        with codecs.open(filepath, 'w', encoding) as f:
            f.write(json.dumps(data,
                               sort_keys=sort_keys,
                               ensure_ascii=ensure_ascii))
    except OSError:
        raise


def get_creation_date(filepath):
    """Get creation date of a file.

    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.

    If modification date is needed, use :meth:`os.path.getmtime` which is
    cross-platform supported.

    Parameters
    ----------
    filepath : str
        Path to file whose creation date will be returned.

    Returns
    -------
    float
        Time of creation in seconds.

    References
    ----------
    Code is from `Stack Overflow's user Mark Amery`_.

    Examples
    --------
    >>> from datetime import datetime
    >>> creation = get_creation_date("/Users/test/directory")
    >>> creation
    1567701693.0
    >>> str(datetime.fromtimestamp(creation))
    '2019-09-05 12:41:33'

    """
    if platform.system() == 'Windows':
        return os.path.getctime(filepath)
    else:
        stat = os.stat(filepath)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


# TODO: test this function
def get_qualname(module, parents=1):
    """TODO

    Parameters
    ----------
    module
    parents : int

    Returns
    -------

    """
    if not isinstance(module, type(os)):
        raise TypeError("'module' must be of type module")
    return ".".join(module.__name__.split(".")[-1-parents:])


def load_json(filepath, encoding='utf8'):
    """Load JSON data from a file on disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file which will be read.
    encoding : str, optional
        Encoding to be used for opening the JSON file in read mode (the default
        value is 'utf8').

    Returns
    -------
    data
        Data loaded from the JSON file.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.

    """
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            data = json.load(f)
    except OSError:
        raise
    else:
        return data


def load_pickle(filepath):
    """Load data from a pickle file on disk.

    The function opens a pickle file and returns its content.

    Parameters
    ----------
    filepath:
        Path to the pickle file

    Returns
    -------
    data
        Content of the pickle file.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.

    """
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
    except OSError:
        raise
    else:
        return data


def load_yaml(filepath):
    """Load the content of a YAML file.

    The content of the YAML file content is returned which is a :obj:`dict`.

    The module :mod:`yaml` needs to be installed. It can be installed with
    ``pip``::

        $ pip install pyyaml

    Parameters
    ----------
    filepath : str
        Path to the YAML file to be read.

    Returns
    -------
    dict
        The dictionary read from the YAML file.

    Raises
    ------
    ImportError
        Raised if the module :mod:`yaml` is not found.
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist or there is an error in the YAML structure of the
        file.

    Notes
    -----
    I got a ``YAMLLoadWarning`` when calling :meth:`yaml.load()` without
    ``Loader``, as the default Loader is unsafe. You must specify a loader with
    the ``Loader=`` argument. See `PyYAML yaml.load(input) Deprecation`_.

    """
    try:
        import yaml
    except ImportError:
        raise ImportError("yaml not found. You can install it with: pip "
                          "install pyyaml")
    try:
        with open(filepath, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except (OSError, yaml.YAMLError) as e:
        raise OSError(e)


def read_file(filepath):
    """Read a file (in text mode) from disk.

    Parameters
    ----------
    filepath : str
        Path to the file to be read from disk.

    Returns
    -------
    str
        Content of the file returned as strings.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.

    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except OSError as e:
        raise


def run_cmd(cmd):
    """Run a command with arguments.

    The command is given as a string but the function will split it in order to
    get a list having the name of the command and its arguments as items.

    Parameters
    ----------
    cmd : str
        Command to be executed, e.g. ::

            open -a TextEdit text.txt

    Returns
    -------
    retcode: int
        Return code which is 0 if the command was successfully completed.
        Otherwise, the return code is non-zero.

    Examples
    --------
    TODO

    """
    try:
        # `check_call()` takes as input a list. Thus, the string command must
        # be split to get the command name and its arguments as items of a list.
        retcode = subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        return e.returncode
    else:
        return retcode


def write_file(filepath, data, overwrite_file=True):
    """Write data (text mode) to a file.

    Parameters
    ----------
    filepath : str
        Path to the file where the data will be written.
    data
        Data to be written.
    overwrite_file : bool, optional
        Whether the file can be overwritten (the default value is True which
        implies that the file can be overwritten).

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.
    OverwriteFileError
        Raised if an existing file is being overwritten and the flag to overwrite
        files is disabled.

    """
    try:
        if os.path.isfile(filepath) and not overwrite_file:
            raise FileExistsError(
                "File '{}' already exists and overwrite is False".format(
                    filepath))
        else:
            with open(filepath, 'w') as f:
                f.write(data)
    except OSError:
        raise
