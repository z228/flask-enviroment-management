from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler

from flask import has_request_context, request
from os import getcwd


class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


log_root_path = getcwd()
task_logging = getLogger("task")
root_logging = getLogger("")
product_logging = getLogger("product")

task_logging.setLevel(10)
root_logging.setLevel(10)
product_logging.setLevel(10)

info_log_path = f'{log_root_path}/logs/flask.log'
debug_log_path = f'{log_root_path}/logs/debug.log'
task_log_path = f'{log_root_path}/logs/task.log'
info_handler = ConcurrentRotatingFileHandler(info_log_path, maxBytes=512 * 1024, backupCount=5,
                                             encoding='utf-8')  # 设置日志字符集和存储路径名字
debug_handler = ConcurrentRotatingFileHandler(debug_log_path, maxBytes=512 * 1024, backupCount=2,
                                              encoding='utf-8')  # 设置日志字符集和存储路径名字
task_handler = ConcurrentRotatingFileHandler(task_log_path, maxBytes=512 * 1024, backupCount=5,
                                             encoding='utf-8')  # 设置日志字符集和存储路径名字
remote_ip_format = RequestFormatter(
    '%(asctime)s - %(remote_addr)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - '
    '%(message)s')
debug_format = RequestFormatter(
    '%(asctime)s - %(remote_addr)s - %(levelname)s - %(message)s')
task_log_format = Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")

info_handler.setFormatter(remote_ip_format)
debug_handler.setFormatter(debug_format)
task_handler.setFormatter(task_log_format)

info_handler.setLevel(20)
debug_handler.setLevel(10)
task_handler.setLevel(20)

task_logging.addHandler(task_handler)
root_logging.addHandler(debug_handler)
product_logging.addHandler(info_handler)
