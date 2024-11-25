import xml.etree.cElementTree as ET
from os.path import join, exists, split, dirname
from os import listdir, chdir, getcwd, popen
from shutil import copy2, rmtree, copytree
from .Excel2Png import gen_xls_diff_png
from logging import getLogger
from ..send_mail import send

task_logger = getLogger("task")
work_path = r'D:\code\python\yhenv\flaskProject\apps\productApp\jobs\genReport'


def get_fail_case(xml_file, root_path, report_path, current_version):
    tree = ET.parse(join(work_path, xml_file))
    root = tree.getroot()
    test_cases = root.findall("testcase")
    root.set('name', f"{current_version}Export.{current_version}ExportTest")
    for case in test_cases:
        fail = case.find('failure')
        if fail is None:
            root.remove(case)
            continue
        msg = fail.get('message')
        if msg is None:
            continue
        text = fail.text
        src_path = r'file:\\\/home'
        replace_path = 'http://192.168.1.199'
        if src_path in text or src_path in msg:
            text = text.replace(src_path, replace_path)
            msg = msg.replace(src_path, replace_path)
        fail.set('message', msg)
        fail.text = text
        if 'The size of the excel file is different:' not in msg:
            continue
        case_name = case.get('name')
        case_diff_fullpath = join(root_path, case_name)
        case_res_fullpath = case_diff_fullpath.replace('diff', 'res')
        case_exp_fullpath = case_diff_fullpath.replace('diff', 'exp')
        case_diff_path, case_start = split(case_diff_fullpath)
        case_res_path = case_diff_path.replace('diff', 'res')
        if not exists(case_diff_path):
            continue
        diff_list = listdir(case_diff_path)
        res_list = listdir(case_res_path)
        diff_sheets = []
        res_sheets = []
        for diff in diff_list:
            sheet_name = diff.replace(f'{case_start}_', '').replace('_diff.jpg', '')
            if '_diff' not in diff or case_start not in diff:
                continue
            # task_logger.info(case_diff_fullpath)
            # task_logger.info(diff)
            # task_logger.info(case_start)
            diff_sheets.append(sheet_name)
        for res in res_list:
            sheet_name = res.replace(f'{case_start}_', '').replace('.png', '')
            if sheet_name in diff_sheets or not sheet_name:
                continue
            if '.png' not in res or case_start not in res:
                continue
            # task_logger.info(case_res_fullpath)
            # task_logger.info(res)
            # task_logger.info(case_start)
            res_sheets.append(sheet_name)
        new_msgs = ''
        if diff_sheets:
            for sheet in diff_sheets:
                exp_path = fr'file:///{case_diff_fullpath}_{sheet}_Exp.jpg'
                res_path = fr'file:///{case_diff_fullpath}_{sheet}_Res.jpg'
                diff_path = fr'file:///{case_diff_fullpath}_{sheet}_diff.jpg'
                exp_msg = f'Exp[<a target="_blank" href={exp_path}>{case_name}_{sheet}_exp</a>]<br/>'
                res_msg = f'Res[<a target="_blank" href={res_path}>{case_name}_{sheet}_res</a>]<br/>'
                diff_msg = f'Diff[<a target="_blank" href={diff_path}>{case_name}_{sheet}_diff</a>]<br/>'
                new_msgs += exp_msg + res_msg + diff_msg
        if res_sheets:
            for sheet in res_sheets:
                exp_path = fr'file:///{case_exp_fullpath}_{sheet}.png'
                res_path = fr'file:///{case_res_fullpath}_{sheet}.png'
                exp_msg = f'Exp[<a target="_blank" href={exp_path}>{case_name}_{sheet}_exp</a>]<br/>'
                res_msg = f'Res[<a target="_blank" href={res_path}>{case_name}_{sheet}_res</a>]<br/>'
                new_msgs += exp_msg + res_msg
        fail.set('message', new_msgs)
    task_logger.info(f'{report_path}\\{xml_file}')
    tree.write(f'{report_path}\\{xml_file}')
    pwd = getcwd()
    chdir(dirname(report_path))
    with popen('ant report') as gen_html:
        res = gen_html.read()
        task_logger.info(res)
    chdir(pwd)


branchs = ['v9.4_test', 'v10.0_test', 'v10.1_test', 'v10.2_test', 'trunk_test']
versions = ['941', '10', '10.1', '10.2', 'trunk']  # 0:v941 、1:v10.0 、2:v10.1 、3：trunk
local_path = r'D:\share\junit_test'
visualcd_suites = ['Chart',
                   #    'CustomerBug',
                   'DBDataprocess',
                   'DBPainter', 'DynamicCalc', 'Export']
module = r"assetExecute\testcases"
res_xml_path = r'assetExecute\reports'
ip_path = r'\\192.168.1.199'
version_count = len(versions)
suite = visualcd_suites[-1]
xml = f'TEST-{suite}.{suite}Test.xml'


def clean_yesterday_res(index):
    current_branch = branchs[index]
    current_version = versions[index]
    root_path = fr'D:\share\export_xls_img\{current_version}\res'
    """
       firstly, generate excel to img(gen_xls_diff_png)
    """
    diff_img_path = root_path.replace('res', 'diff')
    if exists(root_path):
        task_logger.info(f'rm res folder{root_path}')
        rmtree(root_path)
    copytree(join(local_path, current_branch, module, suite, 'res'), root_path)
    if exists(diff_img_path):
        task_logger.info(f'rm diff:{diff_img_path}')
        rmtree(diff_img_path)


def generate_diff_img(index):
    current_version = versions[index]
    root_path = fr'D:\share\export_xls_img\{current_version}\res'
    exp_path = fr'D:\share\export_xls_img\{current_version}\exp'
    with popen(f'svn up {exp_path}') as p2:
        res = p2.read()
    """
       firstly, generate excel to img(gen_xls_diff_png)
    """
    gen_xls_diff_png(root_path, current_version)


def generate_report(index):
    current_branch = branchs[index]
    current_version = versions[index]
    current_version_rm_point = versions[index].replace(".", "")
    new_xml = fr'TEST-{current_version_rm_point}{suite}.{current_version_rm_point}{suite}Test.xml'
    # second, generate html report
    pwd = getcwd()
    copy2(join(ip_path, current_branch, res_xml_path, xml), join(work_path, new_xml))
    get_fail_case(new_xml, fr'D:\share\export_xls_img\{current_version}\diff',
                  r'D:\SVN\trunk\test\assetExecute\reports',
                  current_version_rm_point)


def seq_exec_job():
    for i in range(version_count):
        if i not in [2]:
            task_logger.info(f'{branchs[i]} skip')
            continue
        clean_yesterday_res(i)
        generate_diff_img(i)
        generate_report(i)
    email_text = '<a href="file:///D:/SVN/trunk/test/assetExecute/reports/html/index.html" style="text-decoration: none !important; line-height: 1.5;">点击查看结果</a>'
    send("zengchenglong@yonghongtech.com", "Export Junit Report", email_text)
