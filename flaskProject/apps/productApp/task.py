from logging import getLogger
import os
from shutil import rmtree, copy
from time import strftime, localtime, strptime, sleep
from . import product
from .jobs.send_mail import send
from filecmp import cmp
import subprocess
import psutil

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'D:/old_version/9.3/', 'D:/old_version/trunk/']
path = 'Yonghong_Z-Suite/Yonghong'
jacoco_root_path = r'D:\share\jacoco'
jacoco_199_path = '\\\\192.168.1.199/jacoco/trunk/manual/backup'

productAction = product.ProductAction()
task_logger = getLogger("task")


def read_command(cmd):
    with os.popen(cmd) as p:
        res = p.read()
    return res


def read_command_utf8(cmd):
    with os.popen(cmd) as p:
        try:
            res = p.buffer.read().decode(encoding='utf8')
        except UnicodeDecodeError as e:
            task_logger.error(e)
    return res


def readlines_command(cmd):
    with os.popen(cmd) as p:
        res = p.readlines()
    return res


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
    task_logger.info({'8.6': ['20220926', '20220523']})


def get_now_format_time():
    return strftime('[%Y-%m-%d %H:%M:%S]', localtime())


def diff_day(ftime, fmt):
    """
    calculate days with input and today
    :param ftime:
    :param fmt: format
    :return:
    """
    now_day = eval(strftime("%j", localtime()).lstrip("0"))
    last_day = eval(strftime("%j", strptime(
        ftime[0:4] + '1231', fmt)).lstrip("0"))
    p_day = eval(strftime("%j", strptime(ftime, fmt)).lstrip("0"))
    if ftime[0:4] != strftime("%Y", localtime()):
        return now_day + last_day - p_day
    return now_day - p_day


def delete_temp_file(src, file, filetime):
    if diff_day(filetime, "%Y%m%d") > 30:
        os.remove(f"{src}/{file}")
        task_logger.info(f"delete file：{src}/{file}")


def check_jacoco_file():
    task_logger.info("开始校验jacoco文件")
    os.chdir(jacoco_root_path)
    jacoco_report_path = f"{jacoco_root_path}/trunk/report"
    if os.path.exists(jacoco_report_path):
        rmtree(jacoco_report_path)
    res = read_command('ant report')
    if "BUILD SUCCESSFUL" in res:
        task_logger.info("jacoco文件检验成功")
        task_logger.info(res.split('\n')[-3])
        return True
    task_logger.error(res.split('\n')[-3])
    return False


def get_jacoco_files_list(jacoco_file_path):
    jacoco_files = []
    dos = f'dir /b "{jacoco_file_path}"|findstr zengchenglong'
    all_jacoco = readlines_command(dos)
    for jacoco in all_jacoco:
        if ".exec" in jacoco and "zengchenglong" in jacoco:
            jacoco_files.append(jacoco.replace('\n', ''))
    return jacoco_files


def get_filter_jacoco_files_list(jacoco_file_path):
    jacoco_files = []
    all_jacoco = readlines_command(f'dir "{jacoco_file_path}" |findstr zengchenglong|findstr exec')
    jacoco_files_unchanged = [i.replace('\n', '') for i in all_jacoco]
    for jacoco in jacoco_files_unchanged:
        jacoco_info = jacoco.split()
        if jacoco_info[-2] != "0":
            jacoco_files.append(jacoco.split()[-1])
        else:
            os.remove(f"{jacoco_root_path}/trunk/{jacoco_info[-1]}")
            task_logger.info(f"delete file：{jacoco_info[-1]}")
    return jacoco_files


def compare_jacoco(src, dst, file):
    success_jacoco = []
    if not cmp(f"{src}/{file}", f"{dst}/{file}"):
        task_logger.info("本地文件和199上jacoco文件不同，尝试再次上传")
        copy(f"{src}/{file}", f"{dst}")
        sha256_filea = read_command(
            f'certutil -hashfile {src}/{file} SHA256')
        sha256_fileb = read_command(
            f'certutil -hashfile {dst}/{file} SHA256')
        if sha256_fileb == sha256_filea:
            success_jacoco.append(file)
            delete_temp_file(src, file, file.split('_')[1])
        else:
            task_logger.info(
                f"local SHA256值：{sha256_filea}；199SHA256值：{sha256_fileb}")
    else:
        success_jacoco.append(file)
        delete_temp_file(src, file, file.split('_')[1])
    return success_jacoco


def upload_jacoco_file():
    if not check_jacoco_file():
        task_logger.info("jacoco文件校验失败")
        return False
    jacoco_199_files = get_jacoco_files_list(jacoco_199_path)
    jacoco_local_files = get_filter_jacoco_files_list(
        f'{jacoco_root_path}/trunk')
    subject = "jacoco上传结果通知"
    success_jacoco = []
    for jacoco in jacoco_local_files:
        if jacoco == "jacoco_${DATE}_all.exec":
            task_logger.info(f"跳过文件：{jacoco}")
            continue
        if os.path.getsize(f"{jacoco_root_path}/trunk/{jacoco}") == 0:
            os.remove(f"{jacoco_root_path}/trunk/{jacoco}")
            continue
        if jacoco not in jacoco_199_files:
            task_logger.info(f"开始复制{jacoco}")
            copy(f"{jacoco_root_path}/trunk/{jacoco}", f"{jacoco_199_path}")
            task_logger.info(f'复制{jacoco} 到"{jacoco_199_path}"')
            dos = f'dir "{jacoco_199_path}"|findstr "{jacoco}"'
            task_logger.info(dos + '\n' + read_command(dos))
            success_jacoco.extend(compare_jacoco(fr'{jacoco_root_path}/trunk', jacoco_199_path, jacoco))
            os.remove(f"{jacoco_root_path}/trunk/{jacoco}")
        else:
            delete_temp_file(f'{jacoco_root_path}/trunk', jacoco, jacoco.split('_')[1])
    if success_jacoco:
        upload_jacoco_list = ',\n'.join(success_jacoco)
        content = f"{upload_jacoco_list}成功上传到{jacoco_199_path}"
        send("zengchenglong@yonghongtech.com", subject, content)
    return True


def shutdown_trunk_tomcat():
    productAction.shut_tomcat("trunk")
    task_logger.info("停掉trunk的tomcat进程")


def commit_junit_exp():
    branchs = ['v9.0_test', 'v9.2.1_test',
               'v9.4_test', 'v10.0_test', 'v10.1_test', 'v10.2_test', 'trunk_test']
    visualcd_suites = ['Chart', 'CustomerBug', 'DBDataprocess',
                       'DBPainter', 'DynamicCalc', 'Export']
    msg = 'change exp of junit'
    exp_folders = ['exp', 'exp_dis']
    current_hour = int(localtime()[3])
    if current_hour >= 22 or current_hour <= 9:
        task_logger.info(f'当前时间在22-9点之间，跳过更新')
        return
    for branch in branchs:
        # task_logger.info(branch)
        for suite in visualcd_suites:
            for folder in exp_folders:
                try:
                    svn_exp_path = f'D:\\share\\junit_test\\{branch}\\assetExecute\\testcases\\{suite}\\{folder}'
                    if not os.path.exists(svn_exp_path):
                        continue
                    with os.popen(f'svn cleanup {svn_exp_path}') as p1:
                        r1 = p1.read()
                    # task_logger.info(r1)
                    cases = os.listdir(svn_exp_path)
                    for case in cases:
                        up_path = os.path.join(svn_exp_path, case)
                        if case == 'ParamElem':
                            big_case = os.path.join(up_path, 'ListBox', 'listbox_defaultValue7_编辑可选值v10.pdf')
                            if os.path.exists(big_case):
                                os.remove(big_case)
                                task_logger.info(f'删除超大case：{big_case} 并且跳过更新')
                            continue
                        with os.popen(f'svn up {up_path}') as p2:
                            r2 = p2.read()
                            if len(r2.split('\n')) != 3:
                                task_logger.info(r2)
                        status = readlines_command(f'svn st {up_path}')
                        if not status:
                            continue
                        task_logger.info(status)
                        commit_flag = False
                        for statu in status:
                            st = statu.split()[0]
                            file = statu.split()[1].replace('\n', '')
                            if st == '?':
                                with os.popen(f'svn add {file}') as add:
                                    log = add.read()
                                task_logger.info(f'svn add {file}:' + log)
                                commit_flag = True
                            if st == 'M' or st == 'A':
                                task_logger.info(f'{file} changed:{statu}')
                                commit_flag = True
                        if not commit_flag:
                            continue
                        with os.popen(f'svn ci {up_path} -m "{msg}"') as ci:
                            log = ci.read()
                            task_logger.info(f'svn ci {up_path} -m :result---"{msg}"' + log)
                except Exception as e:
                    task_logger(f'SVN服务器暂时无法连接：{e}')
                    return


def juejin_checkin():
    juejin_src = r'D:\code\python\yhenv\flaskProject\static\job\juejin-helper\workflows'
    os.chdir(juejin_src)
    res = read_command_utf8('npm run checkin')
    task_logger.info(res)


def check_system_memory():
    memory = psutil.virtual_memory()
    info1 = f"可用内存：{round(memory.available / 1000000000, 2)} G"
    info2 = f"已使用内存：{round(memory.used / 1000000000, 2)} G"
    info3 = f"内存使用率：{memory.percent}%"
    return f'{info1}--{info2}--{info3}'


def clean_memory_cache():
    task_logger.info(f'before clean memory:' + check_system_memory())
    subprocess.Popen(r"D:\RAMMap\RAMMap64 -Ew", shell=True).wait()
    subprocess.Popen(r"D:\RAMMap\RAMMap64 -Es", shell=True).wait()
    subprocess.Popen(r"D:\RAMMap\RAMMap64 -Em", shell=True).wait()
    subprocess.Popen(r"D:\RAMMap\RAMMap64 -Et", shell=True).wait()
    subprocess.Popen(r"D:\RAMMap\RAMMap64 -E0", shell=True).wait()
    task_logger.info(f'after clean memory' + check_system_memory())


def test_job(index):
    task_logger.info(f'test_job{index}')


def update_v2ray_geo():
    v2rayn_root_path = r'D:\v2rayN-Core'
    geo_git_path = os.path.joint(v2rayn_root_path, 'v2ray-rules-dat')
    os.chdir(geo_git_path)
    res = read_command_utf8('git pull')
    task_logger.info(res)
    for root, dirs, files in os.walk(v2rayn_root_path, topdown=False):
        if 'v2ray-rules-dat' in root:
            continue
        for file in files:
            if file == 'geoip.dat' or file == 'geosite.dat':
                bash = fr'xcopy {os.path.join(geo_git_path, file)} {root} /Y'
                task_logger.info(read_command_utf8(bash))
                task_logger.info(f'update---{root}---{file} ')
