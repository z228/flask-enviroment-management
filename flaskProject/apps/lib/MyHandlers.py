# coding:utf-8

import codecs
import datetime
import os
from logging.handlers import BaseRotatingHandler


class MidnightRotatingFileHandler(BaseRotatingHandler):
    def __init__(self, filename, maxBytes=0, backupCount=0):
        self.suffix = "%Y-%m-%d.log"
        self.date = datetime.date.today()
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        super(BaseRotatingHandler, self).__init__(filename, mode='a', encoding='utf-8', delay=0)

    def shouldRollover(self, record):
        return self.date != datetime.date.today()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.date = datetime.date.today()

    def _open(self):
        filename = '%s.%s' % (self.baseFilename, self.date.strftime(self.suffix))
        if self.encoding is None:
            stream = open(filename, self.mode)
        else:
            stream = codecs.open(filename, self.mode, self.encoding)
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(filename, self.baseFilename)
        except OSError:
            pass
        return stream
