import os
from . import product
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
from time import strftime, localtime

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
productAction = product.ProductAction()

log_path = f'{os.getcwd()}/logs/task.log'
handler = TimedRotatingFileHandler(log_path, when="D", interval=1, backupCount=10)  # 设置日志字符集和存储路径名字
logging_format = logging.Formatter(  # 设置日志格式
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
logging.getLogger('').addHandler(handler)


def clean_jar():
    for i in to_path:
        back_path = i + path + '/backup_product'
        if os.path.exists(back_path):
            shutil.rmtree(back_path)
        else:
            continue
            pass


def static_clean():
    print('clean---')
    for f in os.listdir('../../static/results'):
        print('删除文件' + f)
        os.remove('../../static/results/' + f)
    for f in os.listdir('../../static/uploads'):
        print('删除文件' + f)
        os.remove('../../static/uploads/' + f)


def Jacoco_change_Jar():
    productAction.restart_tomcat('develop')
    work_dir = r'D:\SVN\trunk\test\assetExecute'
    os.chdir(work_dir)
    os.system('ant test report')


def test_task():
    logging.info("这个是测试task log")


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())
