from logging import getLogger
import os
from shutil import rmtree, copy
from time import strftime, localtime
from . import product

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
jacoco_root_path = r'D:/share/jacoco'
jacoco_199_path = r'\\192.168.1.199/jacoco/trunk/manual'

productAction = product.ProductAction()
task_logger = getLogger("task")


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


def jacoco_change_jar():
    productAction.restart_tomcat('develop')
    work_dir = r'D:\SVN\trunk\test\assetExecute'
    os.chdir(work_dir)
    os.system('ant test report')


def test_task():
    # print("这个是测试task log")
    task_logger.info(f"这个是测试task log{get_now_format_time()}")


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())


def check_jacoco_file():
    task_logger.info("开始校验jacoco文件")
    os.chdir(jacoco_root_path)
    jacoco_report_path = f"{jacoco_root_path}/trunk/report"
    if os.path.exists(jacoco_report_path):
        rmtree(jacoco_report_path)
    res = os.popen('ant report').read()
    if "BUILD SUCCESSFUL" in res:
        task_logger.info("jacoco文件检验成功")
        task_logger.info('\n'.join(res.split('\n')[-3]))
        return True
    task_logger.error('\n'.join(res.split('\n')[-3]))
    return False


def get_jacoco_files_list(jacoco_file_path):
    jacoco_files = [i.replace('\n', '') for i in os.popen(f'dir /b "{jacoco_file_path}"').readlines() if ".exec" in i]
    return jacoco_files


def upload_jacoco_file():
    if not check_jacoco_file():
        task_logger.info("jacoco文件校验失败")
        return False
    jacoco_199_backup_files = get_jacoco_files_list(os.path.join(jacoco_199_path, 'backup'))
    jacoco_199_files = get_jacoco_files_list(jacoco_199_path)
    jacoco_199_files.extend(jacoco_199_backup_files)
    jacoco_local_files = get_jacoco_files_list(f'{jacoco_root_path}/trunk')
    task_logger.info("开始复制jacoco文件")
    for jacoco in jacoco_local_files:
        if jacoco == "jacoco_${DATE}_all.exec":
            continue
        if jacoco not in jacoco_199_files:
            copy(f"{jacoco_root_path}/trunk/{jacoco}",f"{jacoco_199_path}/backup")
            task_logger.info(f'复制{jacoco} 到"{jacoco_199_path}/backup"')
            dos = f'dir "{jacoco_199_path}/backup"|findstr "{jacoco}"'
            task_logger.info(dos+'\n'+os.popen(dos).read())
    return True


def shutdown_trunk_tomcat():
    productAction.shut_tomcat("trunk")
    task_logger.info("停掉trunk的tomcat进程")
