import ast
try:
    # Python 3
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    # Python 2.7
    from ConfigParser import NoOptionError, NoSectionError
    from ConfigParser import SafeConfigParser as ConfigParser
import codecs
from datetime import datetime
import json
import linecache
import logging.config
import os
import pathlib
import platform
import pickle
# TODO: cPickle for Python 2?
import sqlite3
import sys
# Third-party modules
# TODO: check that if it is right to only load modules from third-party when needed
import pytz
import tzlocal
import yaml


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


def create_directory_prompt(dir_path):
    if not os.path.isdir(dir_path):
        print("[ERROR] The directory '{}' doesn't exist".format(dir_path))
        print("Do you want to create the directory {}?".format(dir_path))
        answer = input("Y/N: ").strip().lower().startswith("y")
        if answer:
            print("[INFO] The directory '{}' will be created".format(dir_path))
            # NOTE: only works on Python 3.4+ (however Python 3.4 pathlib is
            # missing `exist_ok` option
            # see https://stackoverflow.com/a/14364249 for different methods of
            # creating directories in Python 2.7+, 3.2+, 3.5+
            pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
            return 0
        else:
            print("[WARNING] The directory '{}' will not be created".format(
                dir_path))
            return 1
    else:
        print("[INFO] Good! The directory '{}' exists".format(dir_path))
        return 0


# Cross-platform code for getting file creation of a file
# ref.: code is from Mark Amery @ https://stackoverflow.com/a/39501288
def creation_date(path_to_file):
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


# update: existing JSON data will not be overwritten, it will be updated with
# the new JSON data
def dump_json(data, path, update=False):
    def dump_data(data, path):
        try:
            with open(path, "w") as f:
                json.dump(data, f)
        except FileNotFoundError:
            print_exception("FileNotFoundError")
            return 1
        else:
            return 0
    if os.path.isfile(path) and update:
        retval = load_json(path)
        if retval is None:
            return 1
        else:
            try:
                assert type(data) == dict
                retval.update(data)
                return dump_data(retval, path)
            except AssertionError:
                print_exception("AssertionError: Type of '{}' is not a dict".format(data))
                return 1
    else:
        return dump_data(data, path)


def dump_json_with_codecs(filepath, data, encoding='utf8', sort_keys=True,
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


def filter_data(data, min_threshold, max_threshold):
    # TODO: every time this function is called, the module is loaded
    import numpy as np
    # Sanity check on input thresholds
    if not (data.max() >= min_threshold >= data.min()):
        min_threshold = data.min()
    if not (data.max() >= max_threshold >= data.min()):
        max_threshold = data.max()
    first_cond = data >= min_threshold
    second_cond = data <= max_threshold
    return np.where(first_cond & second_cond)


def get_data_type(val):
    """
    Given a string, returns its corresponding data type

    ref.: https://stackoverflow.com/a/10261229

    :param val: string value
    :return: Data type of string value
    """
    try:
        t = ast.literal_eval(val)
    except ValueError:
        return str
    except SyntaxError:
        return str
    else:
        if type(t) is bool:
            return bool
        elif type(t) is int:
            return int
        elif type(t) is float:
            return float
        else:
            return str


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
    local_time = None

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


def get_option_value(parser, section, option):
    value_type = get_data_type(parser.get(section, option))
    try:
        if value_type == int:
            return parser.getint(section, option)
        elif value_type == float:
            return parser.getfloat(section, option)
        elif value_type == bool:
            return parser.getboolean(section, option)
        else:
            return parser.get(section, option)
    except NoSectionError:
        print_exception("NoSectionError")
        return None
    except NoOptionError:
        print_exception("NoOptionError")
        return None


def load_json(path):
    data = None
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print_exception("FileNotFoundError")
    return data


def load_json_with_codecs(path, encoding='utf8'):
    data = None
    try:
        with codecs.open(path, 'r', encoding) as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        return data


def load_pickle(path):
    """
    Opens a pickle file and returns its contents or None if file not found.

    :param path: path to the pickle file
    :return: content of the pickle file or None if error
    """
    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    else:
        return data


def load_yaml(f):
    try:
        return yaml.load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(e)


def print_exception(error=None):
    """
    For a given exception, PRINTS filename, line number, the line itself, and
    exception description.

    ref.: https://stackoverflow.com/a/20264059

    :return: None
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    if error is None:
        err_desc = exc_obj
    else:
        err_desc = "{}: {}".format(error, exc_obj)
    # TODO: find a way to add the error description (e.g. AttributeError) without
    # having to provide the error description as input to the function
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), err_desc))


def read_config(config_path):
    parser = ConfigParser()
    found = parser.read(config_path)
    if config_path not in found:
        print("ERROR: {} is empty".format(config_path))
        return None
    options = {}
    for section in parser.sections():
        options.setdefault(section, {})
        for option in parser.options(section):
            options[section].setdefault(option, None)
            value = get_option_value(parser, section, option)
            if value is None:
                print("[ERROR] The option '{}' could not be retrieved from {}".format(option, config_path))
                return None
            options[section][option] = value
    return options


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


def write_file(filepath, data):
    try:
        with open(filepath, 'w') as f:
            f.write(data)
    except OSError as e:
        raise OSError(e)
