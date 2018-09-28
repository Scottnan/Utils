# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wp
# Date: 20180803


# modified by Dawei Chen: if not set up clooger, just print it
# modified by dingo : add qt handler for qt_ui print

import os
import sys
import traceback
import datetime
from datetime import date
import logging
from PyQt5 import QtCore

rootPath = './logs'
ERR_SEP_LINE = '#' * 70

clogger = None  # current logger
logger_name = None

username = os.getenv('USERNAME')
machine = os.getenv('COMPUTERNAME')


class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            # sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            # sys.stderr = XStream._stderr
        return XStream._stderr


def getLogger(name, console_flag=False, ui_flag=True):
    global clogger
    global logger_name

    if clogger is not None:
        if name == logger_name:
            return
        else:
            print("!!!Already set logger: " + logger_name + " will ignore this one: " + name)
            return

    logger_name = name
    clogger = logging.getLogger(name)
    fullpath = rootPath + '/' + name
    filename = fullpath + '/' + date.today().strftime('%Y%m%d') + '.log'

    clogger.setLevel(logging.DEBUG)

    if not os.path.exists(fullpath):
        print(fullpath)
        os.makedirs(fullpath)

    log_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)d\t[%(levelname)s]\t%(message)s', '%Y-%m-%d %H:%M:%S')

    # log_formatter = logging.Formatter(
    #    '%(levelname)s\t%(asctime)s\t[' + username +
    #    '@' + machine + ']\t%(message)s', '%Y-%m-%d %H:%M:%S')

    logfile_handler = logging.FileHandler(filename)
    logfile_handler.setFormatter(log_formatter)
    clogger.addHandler(logfile_handler)

    if console_flag:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        clogger.addHandler(stream_handler)
    if ui_flag:
        qtHandler = QtHandler()
        qt_formatter = logging.Formatter(
            '%(levelname)s\t%(asctime)s.%(msecs)d\t[%(thread)d]\t%(message)s', '%Y-%m-%d %H:%M:%S')
        qtHandler.setFormatter(qt_formatter)
        clogger.addHandler(qtHandler)
        clogger.setLevel(logging.DEBUG)


def error(msg, tb_flag=True):
    if clogger:
        if tb_flag:
            ts = traceback.format_exc().strip()
            if ts != 'None\n':
                msg = '\n'.join([msg, ERR_SEP_LINE, ts, ERR_SEP_LINE])
                msg = msg.strip()
        clogger.error(msg)
    else:
        print(datetime.datetime.now().strftime('ERROR %Y-%m-%d %H:%M:%S.%f ') + msg)


def info(msg):
    if clogger:
        clogger.info(msg)
    else:
        print(datetime.datetime.now().strftime('INFO  %Y-%m-%d %H:%M:%S.%f ') + msg)


def warning(msg):
    if clogger:
        clogger.warning(msg)
    else:
        print(datetime.datetime.now().strftime('WARN  %Y-%m-%d %H:%M:%S.%f ') + msg)


if __name__ == '__main__':
    getLogger('ProductCapitalUtil', console_flag=True)
    info('START')
    info('All Done')

