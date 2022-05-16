from logging import getLogger, Formatter, INFO, DEBUG
from logging.handlers import TimedRotatingFileHandler

from flask import has_request_context, request


class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


task_logging = getLogger("task")
debug_logging = getLogger("debug")
root_logging = getLogger("app")

info_log_path = './logs/flask.log'
debug_log_path = './logs/debug.log'
task_log_path = './logs/task.log'
info_handler = TimedRotatingFileHandler(info_log_path, when="D", interval=1, backupCount=7,
                                        encoding='utf-8')  # 设置日志字符集和存储路径名字
debug_handler = TimedRotatingFileHandler(debug_log_path, when="D", interval=1, backupCount=2,
                                         encoding='utf-8')  # 设置日志字符集和存储路径名字
task_handler = TimedRotatingFileHandler(debug_log_path, when="D", interval=1, backupCount=5,
                                        encoding='utf-8')  # 设置日志字符集和存储路径名字
remote_ip_format = RequestFormatter(
    '%(asctime)s - %(remote_addr)s - requested %(url)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - '
    '%(message)s')
task_log_format = Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
info_handler.setFormatter(remote_ip_format)
debug_handler.setFormatter(remote_ip_format)
task_handler.setFormatter(task_log_format)
info_handler.setLevel(INFO)
debug_handler.setLevel(DEBUG)
task_handler.setLevel(INFO)
task_logging.addHandler(task_handler)
root_logging.addHandler(debug_handler)
root_logging.addHandler(info_handler)
