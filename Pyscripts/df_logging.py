#!/bin/env python3

import sys
from datetime import datetime

def logmsg(msg, filename=None):
    """
    Prints message to stdout and to a file if filename provided.datetime

    :param msg:         The message to be printed
    :param filename:    The name of the file to print the message to. Optional
    :return:            Password from password server
    """

    msg_to_print = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + msg
    print(msg_to_print)
    sys.stdout.flush

    if filename:
        with open(filename, "a") as msgFile:
            msgFile.write(msg_to_print)
            msgFile.close()