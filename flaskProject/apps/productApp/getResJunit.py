from os import makedirs, listdir, walk
from os.path import join, exists, isdir
from json import dump, load
import xml.etree.cElementTree as ET
from shutil import rmtree, copy2
from logging import getLogger
from time import time
import threading
import sys

task_logger = getLogger("task")

branchs = ['v9.2.1_test',
           'v9.4_test', 'v10.0_test', 'v10.1_test', 'v10.2_test', 'trunk_test']
ip_path = '\\\\192.168.1.199'
module = "assetExecute\\testcases"
res_xml_path = 'assetExecute\\reports'
visualcd_suites = ['Chart',
                   #    'CustomerBug',
                   'DBDataprocess',
                   'DBPainter', 'DynamicCalc', 'Export']
res_path = r'D:\\code\\python\\yhenv\\flaskProject\\apps\\productApp\\res'


class copyThread(threading.Thread):
    def __init__(self, remote_file_path, local_file_path):
        threading.Thread.__init__(self)
        self.remote_file_path = remote_file_path
        self.local_file_path = local_file_path

    def run(self):
        copy2(self.remote_file_path, self.local_file_path)


def get_fail_case(branch):
    tree = ET.parse(join(ip_path, branch, res_xml_path,
                         "html\\TESTS-TestSuites.xml"))
    root = tree.getroot()
    module_path = join(ip_path, branch, module)
    suites = listdir(module_path)
    test_suites = root.findall("testsuite")
    fail_cases = {}
    for suite in test_suites:
        suit_name = ''
        for prop in suite.iter("property"):
            if prop.get("name") == "user.dir":
                suit_name += prop.get("value").split('testcases/')[1]
                break
        if suit_name not in visualcd_suites:
            continue
        fail_cases[suit_name] = {}
        for case in suite.iter("testcase"):
            fail = case.findall("failure")
            if not fail:
                continue
            fail_cases[suit_name][str(case.get("name"))] = []
    with open(f'{res_path}\\{branch}_fail_cases.json', 'w', encoding='utf-8') as fail_cases_json:
        dump(fail_cases, fail_cases_json, indent=4, ensure_ascii=False)
        return fail_cases


def get_el_tree_data(branch):
    with open(f'{res_path}\\{branch}_fail_cases_new.json', 'r', encoding='utf-8') as f:
        fail_cases = load(f)
    junit_fail_cases = []
    for suite in fail_cases.keys():
        if not fail_cases[suite]:
            continue
        suites = {"name": suite, "children": []}
        for i in fail_cases[suite].keys():
            if i == 'allFailCaseName':
                continue
            cases = {"name": i, "children": []}
            for j in fail_cases[suite][i]:
                path = i.split('/')
                path[-1] = path[-1].replace(path[-1], j)
                file = {"name": j,
                        "path": f"{suite}/res/{'/'.join(path)}"}
                cases["children"].append(file)
            suites["children"].append(cases)
        junit_fail_cases.append(suites)
    with open(f'{res_path}\\el_tree_{branch}_res.json', 'w', encoding='utf-8') as res_json:
        dump(junit_fail_cases, res_json, indent=4, ensure_ascii=False)
        return junit_fail_cases


def copy_junit_res_to_local(version):
    with open(f'{res_path}\\{version}_test_fail_cases.json', 'r', encoding='utf-8') as f:
        fail_cases = load(f)
    end = fr'{version}_test\assetExecute\testcases'
    remote_path = f'\\\\192.168.1.199\\{version}_test\\assetExecute\\testcases'
    local_path = f'D:\\share\\junit_test\\{version}_test\\assetExecute\\testcases'
    all_suites = listdir(local_path)
    suites = []
    for suite in all_suites:
        if suite == '.svn' or suite not in visualcd_suites or suite not in fail_cases.keys():
            continue
        fail_list = fail_cases[suite]
        if not fail_list:
            continue
        suites.append(suite)
    length = len(suites)

    def copySuiteFile(suite, remote_path, local_path):
        nonlocal fail_cases
        local_res_path = join(local_path, suite, 'res')
        remote_res_path = join(remote_path, suite, 'res')
        if exists(local_res_path):
            rmtree(local_res_path)
        if not exists(remote_res_path):
            return
        task_logger.info(f'{suite} start')
        time_start = time()
        for case in fail_cases[suite].keys():
            if suite == 'DBPainter':
                if 'Tab/' not in case and 'Carousel/' not in case and 'HideOnExport/' not in case:
                    continue
            if '/' not in case:
                continue
            case_list = case.split('/')
            case_name = case_list[-1]
            case_path = join(*case_list[:-1])
            case_full_path = join(remote_res_path, case_path)
            if not exists(case_full_path):
                continue
            for file in listdir(case_full_path):
                if case_name in file:
                    remote_file_path = join(case_full_path, file)
                    local_file_folder_path = case_full_path.replace(
                        remote_res_path, local_res_path)
                    if not exists(local_file_folder_path):
                        makedirs(local_file_folder_path)
                    if isdir(remote_file_path):
                        thread = copyThread(remote_file_path, join(
                            local_file_folder_path, file), True)
                    else:
                        thread = copyThread(remote_file_path, join(
                            local_file_folder_path, file))
                    thread.start()
                    if file not in fail_cases[suite][case]:
                        fail_cases[suite][case].append(file)

        ## 编辑远程文件夹所有文件 然后挨个确认文件名，比较笨，弃用
        # for root, dirs, files in walk(remote_res_path):
        #     for file in files:
        #         if 'listbox_defaultValue7_编辑可选值v10' in file:
        #             continue
        #         remote_file_path = join(root, file)
        #         if not exists(remote_file_path):
        #             continue
        #         local_file_path = root.replace(
        #             remote_res_path, local_res_path)
        #         for case in fail_cases[suite].keys():
        #             case_name = case.split('/')[-1]
        #             case_fold = case.split('/')[-2]
        #             if file.startswith(case_name) and root.endswith(case_fold):
        #                 if not exists(local_file_path):
        #                     makedirs(local_file_path)
        #                 thread = copyThread(remote_file_path, join(
        #                     local_file_path, file))
        #                 thread.start()
        #                 if file not in fail_cases[suite][case]:
        #                     fail_cases[suite][case].append(file)
        #                 break
        time_end = time()
        task_logger.info(f'{suite} cost {int(time_end - time_start)}s')

    class copySuiteThread(threading.Thread):
        def __init__(self, suite, remote_path, local_path):
            threading.Thread.__init__(self)
            self.suite = suite
            self.remote_path = remote_path
            self.local_path = local_path

        def run(self):
            copySuiteFile(self.suite, self.remote_path, self.local_path)
            task_logger.info(f"{self.suite} done")

    threads = []
    for suite in suites:
        thread = copySuiteThread(suite, remote_path, local_path)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
    for i in list(fail_cases.keys()):
        for j in list(fail_cases[i].keys()):
            if not fail_cases[i][j]:
                del fail_cases[i][j]
    with open(f'{res_path}\\{version}_test_fail_cases_new.json', 'w', encoding='utf-8') as fail_cases_json:
        dump(fail_cases, fail_cases_json, indent=4, ensure_ascii=False)


def main():
    for branch in branchs:
        # if branch != 'v10.0_test':
        #     continue
        task_logger.info(branch)
        get_fail_case(branch)
        copy_junit_res_to_local(branch.split('_')[0])
        get_el_tree_data(branch)
        try:
            copy2(f'{res_path}\\el_tree_{branch}_res.json',
                  f'\\\\192.168.0.187\\share\\junit_res\\el_tree_{branch}_res.json')
        except FileNotFoundError as err:
            task_logger.info(err)
            continue
        except:
            task_logger.info("Unexpected error:", sys.exc_info()[0])
            continue
