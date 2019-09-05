"""Module that defines many general and useful functions.

The helpful functions defined here are those that don't relate to databases and
logging since these types of functions are already defined in the ``databases``
and ``logging`` packages.

You will find such functions as for loading a YAML file, writing to a file on
disk, and getting the local time based on the local time zone.

"""

import codecs
from datetime import datetime
import json
import os
import pathlib
import platform
import pickle
# TODO: cPickle for Python 2?
# Third-party modules
# TODO: check that if it is right to only load modules from third-party when
# needed
import pytz
import tzlocal
import yaml
# Custom modules
from utilities.exceptions.files import OverwriteFileError


def add_plural_ending(list_, plural_end="s", singular_end=""):
    """Add plural ending if there are many values in a list.

    If more than one item is found in the list, the function returns by
    default 's'. If not, then the empty string is returned.

    Parameters
    ----------
    list_ : list
        The list that will be checked if a plural or singular ending will be
        returned.
    plural_end : str, optional
        The plural ending (the default value is 's' which implies that 's' will
        be returned in the case that the list contains more than one item).
    singular_end : str, optional
        The singular ending (the default value is '' which implies that nothing
        will be returned in the case that the list contains less than 2 items).

    Returns
    -------
    str
        "s" if more than one item is found in the list, "" (empty string)
        otherwise.

    Examples
    --------
    >>> cars = ["corvette", "ferrari"]
    >>> print("I have {} car{}".format(len(cars), add_plural_ending(cars)))
    I have 2 cars

    >>> pharmacies = ["PharmaOne", "PharmaTwo"]
    >>> print("I went to {} pharmac{}".format(
    ... len(pharmacies),
    ... add_plural_ending(pharmacies, "ies", "y")))
    I went to 2 pharmacies

    >>> pharmacies = ["PharmaOne"]
    >>> print("I went to {} pharmac{}".format(
    ... len(pharmacies),
    ... add_plural_ending(pharmacies, "ies", "y")))
    I went to 1 pharmacy

    """
    return plural_end if len(list_) > 1 else singular_end


def convert_list_to_str(list_):
    """Convert a list of strings into a single string.

    Parameters
    ----------
    list_ : list of str
        List of strings to be converted into a single string.

    Returns
    -------
    str_ : str
        The converted string.

    Examples
    --------
    >>> list_ = ['CA', 'FR', 'US']
    >>> convert_list_to_str(list_)
    "'CA', 'FR', 'US'"

    This function can be useful for building the WHERE condition in SQL
    expressions:
    >>> list_countries = ['CA', 'FR', 'US']
    >>> str_countries = convert_list_to_str(list_countries)
    >>> "SELECT * FROM table WHERE country IN ({})".format(str_countries)
    "SELECT * FROM table WHERE country IN ('CA', 'FR', 'US')"

    """
    str_ = ", ".join(map(lambda a: "'{}'".format(a), list_))
    return str_


def convert_utctime_to_local_tz(utc_time=None):
    """Convert a given UTC time into the local time zone.

    If a UTC time is given, it is converted to the local time zone. If
    `utc_time` is None, then the the current time based on the local time zone
    is returned.

    The date and time is returned as a string with format
    YYYY-MM-DD HH:MM:SS-HH:MM

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
        YYYY-MM-DD HH:MM:SS-HH:MM

    See Also
    --------
    get_current_local_datetime : only returns the current time based on the
                                 local time zone.

    Examples
    --------
    >>> import time
    >>> utc_time = time.gmtime()
    >>> convert_utctime_to_local_tz(utc_time)
    '2019-09-05 18:17:59-04:00'

    """
    # Get the local timezone name
    tz = pytz.timezone(tzlocal.get_localzone().zone)
    if utc_time:
        # Convert ``time.struct_time`` into ``datetime``
        # Only the date and time up to seconds, e.g. (2019, 9, 5, 22, 12, 33)
        utc_time = datetime(*utc_time[:6])
        # Convert time zone unaware ``datetime`` object into aware timezone
        # ``datetime`` object
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


def create_directory(dirpath):
    """Create a directory if it doesn't already exist.

    Parameters
    ----------
    dirpath : str
        Path to directory to be created.

    Raises
    ------
    FileExistsError
        Raised if the directory already exists.
    PermissionError
        Raised if trying to run an operation without the adequate access rights
        - for example filesystem permissions [1].

        Also, on Windows, the ``PermissionError`` can occur if you try to open a
        directory as a file. Though, the error is more accurate in Linux:
        "[Errno 21] Is a directory" [2].

    References
    ----------
    .. [1] `exception PermissionError
    <https://docs.python.org/3/library/exceptions.html#PermissionError>`_.
    .. [2] `PermissionError Errno 13 Permission denied
    <https://stackoverflow.com/a/50759281>`_.

    """
    try:
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=False)
    except FileExistsError as e:
        raise FileExistsError(e)
    except PermissionError as e:
        raise PermissionError(e)


def create_timestamped_directory(parent_dirpath, new_dirname=""):
    """Create a timestamped directory if it doesn't already exist.

    The timestamp is added to the beginning of the directory name, e.g.
    `/Users/test/20190905-122929-documents`.

    Parameters
    ----------
    parent_dirpath : str
        Path to the parent directory.

    new_dirname : str, optional
        Name of the directory to be created (the default value is "" which
        implies that only the timestamp will be added as the name of the
        directory).

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
    new_dirname = "-{}".format(new_dirname) if new_dirname else new_dirname
    timestamped = datetime.now().strftime('%Y%m%d-%H%M%S{dirname}')
    new_dirpath = os.path.join(
        parent_dirpath, timestamped.format(dirname=new_dirname))
    try:
        pathlib.Path(new_dirpath).mkdir(parents=True, exist_ok=False)
    except FileExistsError as e:
        raise FileExistsError(e)
    except PermissionError as e:
        raise PermissionError(e)
    else:
        return new_dirpath


def get_creation_date(filepath):
    """Get creation date of a file.

    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible [1].

    If modification date is needed, use `os.path.getmtime(path)` which is
    cross-platform supported.

    Parameters
    ----------
    filepath : str
        Path to file whose creation date will be returned.

    Returns
    -------
    float
        Time of creation in seconds.

    Notes
    -----
    Code is from StackOverflow's user Mark Amery [1].


    References
    ----------
    .. [1] `How to get file creation & modification date/times in Python?
    StackOverflow <http://stackoverflow.com/a/39501288/1709587>`_.

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


def dumps_json(filepath, data, encoding='utf8', sort_keys=True,
              ensure_ascii=False):
    """Write data to a JSON file.

    The data is first serialized to a JSON formatted ``str`` and then saved
    to disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file where the data will be saved.

    data
        Data to be written to the JSON file.

    encoding : str, optional
        Encoding to be used for opening the JSON file.

    sort_keys : bool, optional
        If *sort_keys* is true, then the output of dictionaries will be sorted
        by key (the default value is True) [1].

    ensure_ascii : bool, optional
        If `ensure_ascii` is false, then the return value can contain
        non-ASCII characters if they appear in strings contained in ``data``.
        Otherwise, all such characters are escaped in JSON strings [2] (the
        default value is False).

    Raises
    ------
    OSError
        Raised if any I/O related occurs while writing the data to disk, e.g.
        the file doesn't exist.

    References
    ----------
    .. [1] ``json.dumps`` docstring description.
    .. [2] ``json.dumps`` docstring description.

    """
    try:
        with codecs.open(filepath, 'w', encoding) as f:
            f.write(json.dumps(data, sort_keys=sort_keys,
                               ensure_ascii=ensure_ascii))
    except OSError as e:
        raise OSError(e)


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
    except OSError as e:
        raise OSError(e)


def get_current_local_datetime():
    """Get the current date and time based on the system's time zone.

    Returns
    -------
    datetime.datetime
        The date and time in the system's time zone.

    See Also
    --------
    convert_utctime_to_local_tz : converts a UTC time based on the system's
                                  time zone.

    Examples
    --------
    >>> datetime_with_tz = get_current_local_datetime()
    >>> datetime_with_tz
    datetime.datetime(2019, 9, 5, 13, 34, 0, 678836, tzinfo=<DstTzInfo
    'US/Eastern' EDT-1 day, 20:00:00 DST>)
    >>> str(datetime_with_tz)
    '2019-09-05 13:34:18.898435-04:00'

    """
    # Get the local timezone name
    tz = pytz.timezone(tzlocal.get_localzone().zone)
    # Get the time in the system's time zone
    return datetime.now(tz)


def init_variable(default, value=None):
    """Get initial value for a variable.

    If the value of the variable is None, the default value is returned.
    Otherwise, the value given is returned.

    Parameters
    ----------
    default
        The default value to be returned if `value` is None.
    value
        The value to be returned if `value` is not None.

    Returns
    -------
    int or float


    Examples
    --------
    >>> var = 'a'
    >>> init_variable('d', var)
    'a'
    >>> var = None
    >>> init_variable(10, var)
    10

    """
    if value is None:
        return default
    else:
        return value


def load_json(filepath, encoding='utf8'):
    """Load JSON data from a file on disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file which will be read.
    encoding : str, optional
        Encoding to be used for opening the JSON file.

    Returns
    -------
    data
        Data loaded from the JSON file.

    Raises
    ------
    OSError
        Raise

    """
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            data = json.load(f)
    except OSError as e:
        raise OSError(e)
    else:
        return data


def load_pickle(filepath):
    """Open a pickle file.

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

    """
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        return data


def load_yaml(f):
    """Load the content of a YAML file.

    Parameters
    ----------
    f
        File stream associated with the file read from disk.

    Returns
    -------
    dict
        The ``dict`` read from the YAML file.

    Raises
    ------
    yaml.YAMLError
        Raised if there is any error in the YAML structure of the file.

    Notes
    -----
    I got a ``YAMLLoadWarning`` when calling `yaml.load()` without `Loader`, as
    the default Loader is unsafe. You must specify a loader with the
    `Loader=` argument. [1]

    References
    ----------
    .. [1] `PyYAML yaml.load(input) Deprecation <https://msg.pyyaml.org/load>`_.

    """
    try:
        return yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(e)


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
        raise OSError(e)


def read_yaml(filepath):
    """Read a YAML file.

    Its content is returned which is a ``dict``.

    Parameters
    ----------
    filepath : str
        Path to the YAML file to be read.

    Returns
    -------
    dict
        The ``dict`` read from the YAML file.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist or an error in the YAML structure of the file.

    """
    try:
        with open(filepath, 'r') as f:
            return load_yaml(f)
    except (OSError, yaml.YAMLError) as e:
        raise OSError(e)


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
        Raised if an existing file is being overwritten.

    """
    try:
        if os.path.isfile(filepath) and not overwrite_file:
            raise OverwriteFileError(
                "File '{}' already exists and overwrite is False".format(
                    filepath))
        else:
            with open(filepath, 'w') as f:
                f.write(data)
    except OSError as e:
        raise OSError(e)
