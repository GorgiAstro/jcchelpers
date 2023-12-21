import os
import jdk
from setuptools import setup
import sys

JDK_VER = '11' # Don't use JDK8, it has a different directory structure......

home_folder = os.path.expanduser('~')
jdk_root_folder = os.path.join(home_folder, ".jdk")

def find_jdk_folder():
    if not os.path.isdir(jdk_root_folder):
        return None

    for file in os.listdir(jdk_root_folder):
        if os.path.isdir(os.path.join(jdk_root_folder, file)) and file.startswith("jdk"):
            file_stripped = file.strip("jdk")
            if file_stripped.startswith("-"):
                file_stripped = file_stripped.strip("-")
            if file_stripped.startswith(JDK_VER):
                return os.path.join(jdk_root_folder, file)

    return None

JDK_HOME = find_jdk_folder() # Find existing JDK installation to avoid downloading it multiple times

if JDK_HOME is None:
    try:
        JDK_HOME = jdk.install(JDK_VER)
    except jdk.JdkError:
        """
        On some machines install-jdk returns permission error due to the file permissions of some files in the JDK archive,
        and does not return the path, but still unzips the JDK successfully. Therefore we catch the exception and look
        manually for the JDK folder.
        """
        JDK_HOME = find_jdk_folder()

if JDK_HOME is None:
    raise IOError(f"For some reason, the JDK could not be downloaded and extracted to {jdk_root_folder}")

if sys.platform == "darwin":
    JDK_HOME = os.path.join(JDK_HOME, "Contents", "Home")

with open(os.path.join("helpers3", "config.py"), "w") as f:
    f.writelines([
        f'JDK_VER={JDK_VER}\n',
        f'JDK_HOME=r"{JDK_HOME}"'
    ])

setup()