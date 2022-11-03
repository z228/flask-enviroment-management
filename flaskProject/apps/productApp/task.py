from cmath import exp
import os
from filecmp import cmpfiles
from re import S
from shutil import rmtree, copytree
from time import strftime, strptime, localtime, sleep
from . import product
from logging import getLogger
from apps.lib.send_mail import send

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
productAction = product.ProductAction()
config = productAction.config
version = []
for i in config.keys():
    if config[i]['branch'] not in version:
        version.append(config[i]['branch'])
product_path = r'/home/share'
cache_path = r'/home/share/cache.txt'
ip_dist = r'/home/share/version/'
ip_source = r'/mnt/134/productJar/version/'
jacoco_192_path = r'/mnt/192/jacoco/trunk'
jacoco_local_path = r'/opt/jacoco/trunk'
file_list = ['api.jar', 'product.jar', 'thirds.jar']
task_logger = getLogger("task")
jar_list = {}

def read_command(cmd):
    with os.popen(cmd) as p:
        res = p.read()
    return res

def readlines_command(cmd):
    with os.popen(cmd) as p:
        res = p.readlines()
    return res

def get_jar_list():
    """
    get jar list from ip_187 and ip_134
    :return:
    """
    for key in config.keys():
        branch = config[key]["branch"]
        dir_187 = os.listdir(f'{productAction.ip_187}{branch}') if os.path.exists(
            f'{productAction.ip_187}{branch}') else []
        dir_134 = os.listdir(f'{productAction.ip_134}{branch}')
        dir_134.extend(dir_187)
        dir_list = productAction.clear_list_dumplicate(dir_134)
        jar_list[key] = dir_list
        jar_list[key] = productAction.clear_list_not_num(jar_list[key])
        jar_list[key].sort()
        jar_list[key].reverse()


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
        backup_folders = read_command(
            f"ls {os.path.join(product_path, i)}").split()
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
        subject = f"{v} 新的Jar包 已更新"
        part0 = """<!DOCTYPE html>
<html>
<head>
    <meta. charset="UTF-8">
        <title>jar包更新</title>
</head>
<body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" ffset="0">
<div style="font-size: 14pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
<p>
"""
        part2 = """</div></body>
</html>"""
        path0 = ip_134_today.replace('/mnt/134/productJar', '134\git-package')
        path1 = ip_today.replace('/home', '187')
        content = f"{path0} update to {path1}"
        content0 = "</p><p><small>取包的路径：</small><br><small>#1.\\\\192.168.0.187\share（账户密码：<b>tkl-share/9926</b>）</small><br><small>#2.\\\\192.168.0.141\productJar（账户密码：<b>cdqa/yonghong@123</b>）</small></p>"
        task_logger.info(content)
        send("qa-visualcd@yonghongtech.com", subject,
             part0 + content + content0 + part2)
    except PermissionError:
        bash = f"echo '{ip_134_today}/{v}be tied up,please wait...time{get_now_format_time()}\n'>> {cache_path}"
        os.system(bash)
        task_logger.info(f"{ip_134_today}/{v}be tied up,please wait...")


def test_task():
    print(f"{get_now_format_time()}测试定时任务的运行")


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())


def copy_jacoco_to_192():
    read_command(
        f'\mv -f {jacoco_local_path}/*zengchenglong3.exec {jacoco_192_path}')


def test_svn():
    status = read_command(
        f'svn st /home/share/junit_test/v9.0_test/assetExecute/testcases/Chart/exp')
    task_logger.info(status)


def commit_junit_exp():
    branchs = ['v9.0_test', 'v9.2.1_test',
               'v9.4_test', 'v10.0_test', 'trunk_test']
    visualcd_suites = ['Chart', 'CustomerBug', 'DBDataprocess',
                       'DBPainter', 'DynamicCalc', 'Export']
    msg = 'change exp of junit'
    for branch in branchs:
        task_logger.info(branch)
        for suite in visualcd_suites:
            svn_exp_path = f'/home/share/junit_test/{branch}/assetExecute/testcases/{suite}/exp'
            # os.chdir(svn_exp_path)
            os.popen(f'svn up {svn_exp_path}')
            sleep(10)
            os.popen(f'svn cleanup {svn_exp_path}')
            sleep(10)
            task_logger.info(f'svn st {svn_exp_path}')
            status = os.popen(f'svn st {svn_exp_path}').readlines()
            if not status:
                task_logger.info(f"{branch}的{suite}没有修改")
                continue
            task_logger.info(status)
            for statu in status:
                st = statu.split()[0]
                file = statu.split()[1].replace('\n', '')
                if st == '?':
                    log = os.popen(f'svn add {file}').read()
                    task_logger.info(log)
            log = os.popen(f'svn ci {svn_exp_path} -m "{msg}"').read()
            task_logger.info(log)


get_jar_list()
