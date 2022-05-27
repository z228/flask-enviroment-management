import os
from filecmp import cmpfiles
from shutil import rmtree, copytree
from time import strftime, strptime, localtime
from . import product
from logging import getLogger

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
productAction = product.ProductAction()
config = productAction.config
version = [config[i]['branch'] for i in config.keys()]
product_path = r'/home/share'
cache_path = r'/home/share/cache.txt'
ip_dist = r'/home/share/version/'
ip_source = r'/mnt/134/productJar/version/'
jacoco_192_path = r'/mnt/192/jacoco/trunk'
jacoco_local_path = r'/opt/jacoco/trunk'
file_list = ['api.jar', 'product.jar', 'thirds.jar']
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


def kill_trunk_tomcat():
    productAction.shut_tomcat('trunk', 'system')
    task_logger.info(f'杀死trunk tomcat进程')


def killall_java():
    kill_trunk_tomcat()
    os.system('killall -9 java')
    task_logger.info(f'杀死所有java进程')


def bool_cmp(a, b, common):
    result_list = cmpfiles(a, b, common)[0]
    for i in common:
        if i not in result_list:
            return False
    else:
        return True


def diff_day(ftime, fmt):
    """
    calculate days with input and today
    :param ftime:
    :param fmt: format
    :return:
    """
    now_day = eval(strftime("%j", localtime()).lstrip("0"))
    p_day = eval(strftime("%j", strptime(ftime, fmt)).lstrip("0"))
    return now_day - p_day


def clean_backup_jar():
    os.system(f"rm {os.path.join(product_path, 'cache.txt')}")
    for i in version:
        backup_folders = os.popen(f"ls {os.path.join(product_path, i)}").read().split()
        if len(backup_folders) <= 5:
            continue
        for j in backup_folders:
            if diff_day(j, "%Y%m%d") > 5:
                bash = f"rm -R {os.path.join(product_path, i, j)}"
                os.system(bash)
                os.system(f"echo {bash} >>{product_path}/cache.txt")
                task_logger.info(bash)


def copy_jar_to_local():
    """
    copy jar to local
    :return:
    """
    for v in version:
        today = strftime("%Y%m%d", localtime())
        ip_today = f"{ip_dist.replace('version', v)}{today}"
        ip_134_today = f"{ip_source.replace('version', v)}{today}"
        if os.path.exists(ip_134_today):
            if not os.path.exists(ip_today):
                bash = f"mkdir -p {ip_today}"
                os.system(bash)
                task_logger.info(bash)
                try_copy(v, ip_today, ip_134_today)
            if not bool_cmp(ip_today, ip_134_today, file_list):
                try_copy(v, ip_today, ip_134_today)


def try_copy(v, ip_today, ip_134_today):
    try:
        copytree(ip_134_today, ip_today)
        bash = f"echo '{ip_134_today} update time{get_now_format_time()}\n'>> {cache_path}"
        os.system(bash)
        task_logger.info(f"{ip_134_today} update")
    except PermissionError:
        bash = f"echo '{ip_134_today}/{v}be tied up,please wait...time{get_now_format_time()}\n'>> {cache_path}"
        os.system(bash)
        task_logger.info(f"{ip_134_today}/{v}be tied up,please wait...")


def test_task():
    print(f"{get_now_format_time()}测试定时任务的运行")


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())


def copy_jacoco_to_192():
    os.popen(f'/mv -f {jacoco_local_path}/*.exec {jacoco_192_path}')
