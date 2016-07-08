# -*- coding: utf-8 -*-
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler


class MyLogger(object):
    def __init__(self, logfile_name=None):
        try:
            self.logfile = ""
            if not logfile_name:
                self.logfile = './socketio_api.log'
            else:
                self.logfile = './{0}.log'.format(logfile_name)
        except Exception, e:
            print "@@ MyLogger __init__ except {0}".format(e)
            pass

    def init_logger(self, logger_name, to_file=True, to_console=False):
        if logger_name not in Logger.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)

            if to_console:
                # all to console and it will into kodi log file
                datefmt = "%Y-%m-%d %H:%M:%S"
                # format_str = '[%(asctime)s]: TID-%(thread)d [%(name)s] (%(levelname)s) L#%(lineno)s : %(message)s'
                format_str = '[%(asctime)s]: %(name)s (%(levelname)s) L#%(lineno)s : %(message)s'
                formatter = logging.Formatter(format_str, datefmt)
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.INFO)
                logger.addHandler(console_handler)

            if to_file:
                # handler all
                handler = RotatingFileHandler(
                    self.logfile, mode='a', maxBytes=1024000, backupCount=5)
                datefmt = "%Y-%m-%d %H:%M:%S"
                format_str = '[%(asctime)s]: %(name)s (%(levelname)s) L#%(lineno)s %(message)s'
                # format_str = '[%(asctime)s]: TID-%(thread)d [%(name)s] (%(levelname)s) L#%(lineno)s : %(message)s'
                formatter = logging.Formatter(format_str, datefmt)
                handler.setFormatter(formatter)
                handler.setLevel(logging.INFO)
                logger.addHandler(handler)
                """
                # handler error
                handler = RotatingFileHandler('/tmp/ktv_error.log', mode='a', maxBytes=1024000, backupCount=5)
                datefmt = "%Y-%m-%d %H:%M:%S"
                format_str = "[%(asctime)s]: %(name)s %(levelname)s L%(lineno)s %(message)s"
                formatter = logging.Formatter(format_str, datefmt)
                handler.setFormatter(formatter)
                handler.setLevel(logging.ERROR)
                logger.addHandler(handler)
                """
        logger = logging.getLogger(logger_name)
        return logger


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
