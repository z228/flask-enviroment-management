import os
from os.path import join
from json import dump, load
import xml.etree.cElementTree as ET
import re
from logging import getLogger
from shutil import copy
from tqdm import tqdm

task_logger = getLogger("task")
branchs = ['v8.6_test','v9.0_test','v9.2.1_test','v9.4_test','trunk_test']
ip_path = r'/mnt/199'
module = r"assetExecute/testcases"
res_xml_path = r'assetExecute/reports'
cwd_path = os.path.dirname(os.path.abspath(__file__))

def get_fail_case_list(branch):
    tree = ET.parse(join(ip_path,branch,res_xml_path,r"html/TESTS-TestSuites.xml"))
    root = tree.getroot()
    module_path  = join(ip_path,branch,module)
    suites = os.listdir(module_path)
    test_suites = root.findall("testsuite")
    fail_cases = {}
    res = []
    for suite in tqdm(test_suites):
        suit_name = ''
        for prop in suite.iter("property"):
            if prop.get("name") == "user.dir":
                suit_name += prop.get("value").split('testcases/')[1]
                break
        fail_cases[suit_name] = []
        for case in suite.iter("testcase"):
            fail = case.findall("failure")
            if not fail:
                continue
            fail_cases[suit_name].append(str(case.get("name")))
        # fail_cases.append(fail_case)
    with open(f'{cwd_path}/{branch}_fail_cases.json', 'w', encoding='utf-8') as fail_cases_json:
        dump(fail_cases, fail_cases_json, indent=4, ensure_ascii=False)
    for suite in tqdm(fail_cases.keys()):
        if not fail_cases[suite]:
            continue
        res_path = join(module_path,suite,'res')
        for res_folder_path in fail_cases[suite]:
            case_name  = res_folder_path.split('/')[-1] if '/' in res_folder_path else res_folder_path
            case_path = '/'.join(res_folder_path.split('/')[0:-1]) if '/' in res_folder_path else ''
            for (root, dirs, files) in os.walk(join(res_path,case_path)):
                if not files:
                    continue
                folder = root.split('/res/')[1] if '/res/' in root else ''
                for file in files:
                    if case_name not in file:
                        continue
                    res.append({
                        "branch":branch.split('_test')[0],
                            "path":root,
                            "file":file,
                            "module":suite,
                            "folder":folder})
    with open(f'{cwd_path}/{branch}_res.json','w', encoding='utf-8') as res_json:
        dump(res, res_json, indent=4, ensure_ascii=False)
    
    
# get_fail_case_list('v9.4_test')

def get_junit_res(branch):
    branch = f"{branch}_test" if '_test' not in branch else branch
    with open(f'{cwd_path}/{branch}_res.json','r',encoding='utf-8') as res_json:
        res = load(res_json)
    return res
    
def copy_junit_res(branch,files):
    for file in files:
        copy(join(file['path'],file['file']),join(local_))