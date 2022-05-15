import os
from filecmp import cmpfiles
from shutil import rmtree, copytree
from time import strftime, strptime, localtime

from . import product

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
productAction = product.ProductAction()
version = ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']
product_path = r'/home/share'
cache_path = r'/home/share/cache.txt'
ip_dist = r'/home/share/version/'
ip_source = r'/mnt/134/productJar/version/'
file_list = ['api.jar', 'product.jar', 'thirds.jar']


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


def bool_cmp(a, b, common):
    result_list = cmpfiles(a, b, common)[0]
    for i in common:
        if i not in result_list:
            return False
    else:
        return True


def diff_day(ftime, fmt):
    now_day = eval(strftime("%j", localtime()).lstrip("0"))
    p_day = eval(strftime("%j", strptime(ftime, fmt)).lstrip("0"))
    return now_day - p_day


def clean_backup_jar():
    os.system(f"rm {os.path.join(product_path, 'cache.txt')}")
    for i in version:
        backup_folders = os.popen(f"ls {os.path.join(product_path, i)}").read().split()
        if len(backup_folders) < 5:
            continue
        for j in backup_folders:
            if diff_day(j, "%Y%m%d") > 5:
                os.system(f"rm -R {os.path.join(product_path, i, j)}")
                bash = f"rm -R {os.path.join(product_path, i, j)}"
                os.system(f"echo {bash} >>{product_path}/cache.txt")


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())


def copy_jar_to_local():
    for v in version:
        today = strftime("%Y%m%d", localtime())
        ip_today = f"{ip_dist.replace('version', v)}{today}"
        ip_134_today = f"{ip_source.replace('version', v)}{today}"
        if os.path.exists(ip_134_today):
            if not os.path.exists(ip_today):
                os.system(f"mkdir {ip_today}")
                try:
                    copytree(ip_134_today, ip_today)
                    os.system(
                        f"echo '{ip_134_today} update time{get_now_format_time()}\n'>> {cache_path}")
                except PermissionError:
                    os.system(
                        f"echo '{ip_134_today}/{v}be tied up,please wait...time{get_now_format_time()}\n'>> {cache_path}")
            else:
                if not bool_cmp(ip_today, ip_134_today, file_list):
                    try:
                        copytree(ip_134_today, ip_today)
                        os.system(
                            f"echo '{ip_134_today} update time{get_now_format_time()}\n'>> {cache_path}")
                    except PermissionError:
                        os.system(
                            f"echo '{ip_134_today}/{v}be tied up,please wait...time{get_now_format_time()}\n'>> {cache_path}")


def test_task():
    print("测试定时任务的运行")
