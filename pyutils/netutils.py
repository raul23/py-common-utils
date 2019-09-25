"""Module that defines networking-related functions.

Extended module summary

"""

import os
import platform
import subprocess


def get_platform():
    """

    Returns
    -------

    """
    return platform.system().lower()


def notify(title, text):
    """

    Parameters
    ----------
    title
    text

    Returns
    -------

    """
    # TODO: add ref
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def ping_alive(host):
    """

    Parameters
    ----------
    host

    Returns
    -------

    """
    try:
        arg = "-{}1".format('n' if get_platform() == "windows" else 'c')
        subprocess.check_call(['ping', arg, host])
    except subprocess.CalledProcessError as e:
        # TODO: raise instead of print
        print(e)
        return False
    return True
