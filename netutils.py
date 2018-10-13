import os
import platform
import subprocess


def get_platform():
    return platform.system().lower()


def ping_alive(host):
    try:
        arg = "-{}1".format('n' if get_platform() == "windows" else 'c')
        subprocess.check_call(['ping', arg, host])
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    return True


def notify(title, text):
    # TODO: add ref
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
