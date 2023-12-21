import os
import jdk
from setuptools import setup
import sys

JDK_VER = '11' # Don't use JDK8, it has a different directory structure......
JDK_HOME = None
try:
    JDK_HOME = jdk.install(JDK_VER)
except jdk.JdkError:
    home_folder = os.path.expanduser('~')
    jdk_root_folder = os.path.join(home_folder, ".jdk")
    for file in os.listdir(jdk_root_folder):
        if os.path.isdir(os.path.join(jdk_root_folder, file)) and file.startswith("jdk"):
            file_stripped = file.strip("jdk")
            if file_stripped.startswith("-"):
                file_stripped = file_stripped.strip("-")
            if file_stripped.startswith(JDK_VER):
                JDK_HOME = os.path.join(jdk_root_folder, file)
                break

if sys.platform == "darwin":
    JDK_HOME = os.path.join(JDK_HOME, "Contents", "Home")

with open(os.path.join("helpers3", "config.py"), "w") as f:
    f.writelines([
        f'JDK_VER={JDK_VER}\n',
        f'JDK_HOME=r"{JDK_HOME}"'
    ])

setup()