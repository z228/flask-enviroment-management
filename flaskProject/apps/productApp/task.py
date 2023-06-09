from logging import getLogger
import os
from shutil import rmtree, copy
from time import strftime, localtime, strptime, sleep
from . import product
from .send_mail import send
from filecmp import cmp

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
        if jacoco not in jacoco_199_files:
            task_logger.info(f"开始复制{jacoco}")
            copy(f"{jacoco_root_path}/trunk/{jacoco}", f"{jacoco_199_path}")
            task_logger.info(f'复制{jacoco} 到"{jacoco_199_path}"')
            dos = f'dir "{jacoco_199_path}"|findstr "{jacoco}"'
            task_logger.info(dos + '\n' + read_command(dos))
            success_jacoco.extend(compare_jacoco(fr'{jacoco_root_path}/trunk', jacoco_199_path, jacoco))
        else:
            delete_temp_file(f'{jacoco_root_path}/trunk', jacoco, jacoco.split('_')[1])
    upload_jacoco_list = ',\n'.join(success_jacoco)
    content = f"{upload_jacoco_list}成功上传到{jacoco_199_path}"
    send("zengchenglong@yonghongtech.com", subject, content)
    return True


def shutdown_trunk_tomcat():
    productAction.shut_tomcat("trunk")
    task_logger.info("停掉trunk的tomcat进程")


def commit_junit_exp():
    branchs = ['v9.0_test', 'v9.2.1_test',
               'v9.4_test', 'v10.0_test', 'trunk_test']
    visualcd_suites = ['Chart', 'CustomerBug', 'DBDataprocess',
                       'DBPainter', 'DynamicCalc', 'Export']
    msg = 'change exp of junit'
    exp_folders = ['exp', 'exp_dis']
    for branch in branchs:
        # task_logger.info(branch)
        for suite in visualcd_suites:
            for folder in exp_folders:
                svn_exp_path = f'D:\\share\\junit_test\\{branch}\\assetExecute\\testcases\\{suite}\\{folder}'
                if not os.path.exists(svn_exp_path):
                    continue
                # os.chdir(svn_exp_path)
                with os.popen(f'svn cleanup {svn_exp_path}') as p1:
                    r1 = p1.read()
                # task_logger.info(r1)
                with os.popen(f'svn up {svn_exp_path}') as p2:
                    r2 = p2.read()
                # task_logger.info(r2)
                # task_logger.info(f'svn st {svn_exp_path}')
                status = readlines_command(f'svn st {svn_exp_path}')
                if not status:
                    # task_logger.info(f"{branch}的{suite}没有修改")
                    continue
                task_logger.info(status)
                commit_flag = False
                for statu in status:
                    st = statu.split()[0]
                    file = statu.split()[1].replace('\n', '')
                    if st == '?':
                        with os.popen(f'svn add {file}') as add:
                            log = add.read()
                        task_logger.info(log)
                    if st == 'M':
                        commit_flag = True
                if not commit_flag:
                    continue
                with os.popen(f'svn ci {svn_exp_path} -m "{msg}"') as ci:
                    log = ci.read()
                task_logger.info(log)


def juejin_checkin():
    juejin_src = r'D:\code\python\yhenv\flaskProject\static\job\juejin-helper\workflows'
    os.chdir(juejin_src)
    res = read_command_utf8('yarn checkin')
    task_logger.info(res)


