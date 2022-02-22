import datetime
import sys

import psutil


def memory():
    return "{:.4} MB".format(psutil.Process().memory_info().rss / 1024**2)


def py_ver():
    return ".".join([str(v) for v in sys.version_info[:3]])


def uptime(start_time):
    return str(datetime.datetime.utcnow() - start_time)[2:][:5]
