import codecs
from datetime import datetime
import json
import logging.config
import os
import pathlib
import platform
import pickle
# TODO: cPickle for Python 2?
import sqlite3
# Third-party modules
# TODO: check that if it is right to only load modules from third-party when
# needed
import pytz
import tzlocal
import yaml
# Own modules
from .exc import OverwriteFileError
from utilities.custom_logging.logging_wrapper import LoggingWrapper


def add_plural(v, plural_end="s", singular_end=""):
    return plural_end if v > 1 else singular_end


def connect_db(db_path, autocommit=False):
    """
    Creates a database connection to the SQLite database specified by the
    `db_path`

    :param db_path: path to database file
    :param autocommit: TODO
    :return: sqlite3.Connection object  or None
    """
    try:
        if autocommit:
            conn = sqlite3.connect(db_path, isolation_level=None)
        else:
            conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(e)


# Useful for building SQL expressions
def convert_list_to_str(list_):
    str_ = ", ".join(
        map(lambda a: "'{}'".format(a), list_))
    return str_


def create_directory(dirpath):
    if os.path.isdir(dirpath):
        raise ResourceWarning(
            "The directory '{}' already exists!".format(dirpath))
    try:
        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(e)


def create_directory_prompt(dirpath):
    if not os.path.isdir(dirpath):
        print("[ERROR] The directory '{}' doesn't exist".format(dirpath))
        print("Do you want to create the directory {}?".format(dirpath))
        answer = input("Y/N: ").strip().lower().startswith("y")
        if answer:
            print("[INFO] The directory '{}' will be created".format(dirpath))
            # NOTE: only works on Python 3.4+ (however Python3.4 pathlib is
            # missing the `exist_ok` option
            # see https://stackoverflow.com/a/14364249 for different methods of
            # creating directories in Python 2.7+, 3.2+, 3.5+
            pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
            return 0
        else:
            print("[WARNING] The directory '{}' will not be created".format(
                dirpath))
            return 1
    else:
        print("[INFO] Good! The directory '{}' exists".format(dirpath))
        return 0


def create_timestamped_directory(new_fname, parent_dirpath):
    timestamped = datetime.now().strftime('%Y%m%d-%H%M%S-{fname}')
    new_dirpath = os.path.join(
        parent_dirpath, timestamped.format(fname=new_fname))
    try:
        pathlib.Path(new_dirpath).mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(e)
    else:
        return new_dirpath


# Cross-platform code for getting file creation of a file
# ref.: code is from Mark Amery @ https://stackoverflow.com/a/39501288
def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.

    If modification date is needed, use os.path.getmtime(path) which is
    cross-platform supported.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def dump_json(filepath, data, encoding='utf8', sort_keys=True,
              ensure_ascii=False):
    try:
        with codecs.open(filepath, 'w', encoding) as f:
            f.write(json.dumps(data, sort_keys=sort_keys,
                               ensure_ascii=ensure_ascii))
    except OSError as e:
        raise OSError(e)


def dump_pickle(filepath, data):
    """
    Dumps a pickle file on disk and returns TODO: writeme

    :param filepath: absolute path to the pickle file where data will be written
    :param data: data to be saved on disk
    :return: TODO: writeme
    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)


# Returns a `datetime` from the local time zone
def get_local_datetime():
    # Get the local timezone name
    tz = pytz.timezone(tzlocal.get_localzone().zone)
    # Get the time in the system's time zone
    return datetime.now(tz)


def get_local_time(utc_time=None):
    """
    If a UTC time is given, it is converted to the local time zone. If
    `utc_time` is None, then the local time zone is simply returned.
    The local time zone is returned as a string with format
    YYYY-MM-DD HH:MM:SS-HH:MM

    :param utc_time: object of type `time.struct_time`
    :return local_time: string representing the local time
    """
    # Get the local timezone name
    tz = pytz.timezone(tzlocal.get_localzone().zone)
    if utc_time:
        # Convert time.struct_time into datetime
        utc_time = datetime(*utc_time[:6])
        # Convert naive object (time zone unaware) into aware object
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


def get_logger(module_name, module_file, cwd, logger):
    if isinstance(logger, dict):
        from utilities.custom_logging.logging_boilerplate import LoggingBoilerplate
        lb = LoggingBoilerplate(module_name,
                                module_file,
                                cwd,
                                logger)
        return lb.get_logger()
    else:
        # Sanity check on `logger`
        if isinstance(logger, LoggingWrapper):
            return logger
        else:
            # TODO: test error
            raise TypeError("`logger` must be of type `LoggingWrapper`")


def init_variable(v, default):
    if v is None:
        return default
    else:
        return v


def load_json(path, encoding='utf8'):
    try:
        with codecs.open(path, 'r', encoding) as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        return data


def load_pickle(filepath):
    """
    Opens a pickle file and returns its contents or raises FileNotFoundError if
    file not found.

    :param filepath: path to the pickle file
    :return: content of the pickle file
    """
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        return data


def load_yaml(f):
    try:
        # IMPORTANT: I got a YAMLLoadWarning when calling `yaml.load()` without
        # `Loader=...` [deprecated], as the default Loader is unsafe.
        # Ref.: https://msg.pyyaml.org/load or https://bit.ly/2ZuYSrD
        # You must specify a loader with the `Loader=` argument
        return yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(e)


def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except OSError as e:
        raise OSError(e)


def read_yaml_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return load_yaml(f)
    except (OSError, yaml.YAMLError) as e:
        raise OSError(e)


# Setup logging from YAML configuration file or logging `dict`
def setup_logging(logging_config, add_datetime=False):
    try:
        if isinstance(logging_config, str):
            # Read YAML configuration file
            config_dict = read_yaml_config(logging_config)
        else:
            config_dict = logging_config
        if add_datetime:
            # Add the datetime to the beginning of the log filename
            # ref.: https://stackoverflow.com/a/45447081
            filename = config_dict['handlers']['file']['filename']
            new_filename = '{:%Y-%m-%d-%H-%M-%S}-{}'.format(
                datetime.now(), filename)
            config_dict['handlers']['file']['filename'] = new_filename
        # Update the logging config dict with new values from `config_dict`
        logging.config.dictConfig(config_dict)
    except OSError as e:
        raise OSError(e)
    except KeyError as e:
        raise KeyError(e)
    except ValueError as e:
        raise ValueError(e)
    else:
        return config_dict


def write_file(filepath, data, overwrite_file=True):
    try:
        if os.path.isfile(filepath) and not overwrite_file:
            raise OverwriteFileError("File '{}' already exists and `overwrite` "
                                     "is False".format(filepath))
        else:
            with open(filepath, 'w') as f:
                f.write(data)
    except OSError as e:
        raise OSError(e)
