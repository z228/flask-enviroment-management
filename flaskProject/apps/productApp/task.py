import os
from . import product
from shutil import rmtree
import os
from time import strftime, strptime , localtime

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
productAction = product.ProductAction()
version = ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']
product_path = r'/home/share'


def clean_backup_jar():
    for i in version:
        for j in os.popen(f"ls {os.path.join(product_path, i)}").read().split():
            if diffDay(j, "%Y%m%d") > 5:
                os.system(f"rm -R {os.path.join(product_path, i, j)}")


def clean_jar():
    for i in to_path:
        back_path = i + path + '/backup_product'
        if os.path.exists(back_path):
            rmtree(back_path)
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


def killall_java():
    os.system('killall -9 java')
    # current_app.logger.info(f'杀死所有java进程')


def diffDay(ftime, fmt):
    nowDay = eval(strftime("%j", localtime()).lstrip("0"))
    pDay = eval(strftime("%j", strptime(ftime, fmt)).lstrip("0"))
    return nowDay - pDay
