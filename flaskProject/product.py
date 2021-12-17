from ntpath import join
import os
import signal
import time
from shutil import copy2, rmtree
import filecmp
import socket
from task import clean_jar
import json
import win32api as api
import win32console as con
from flask import current_app


host_ip = '127.0.0.1'
ip = '\\\\192.168.0.141/productJar/'
ip_134 = '\\\\192.168.1.134/git-package/'
from_path = []
script_path = r"C:\Users\228\PycharmProjects\flaskProject\static\job"
to_path = []
day_31 = ['02', '04', '06', '08', '09', '11']
port = []
ubuntu_path = []
current_system = "windows"
codeType = {"default": ".py", "application/json": ".json", "sql": ".sql", "javascript": ".js", "css": ".css",
            "xml": ".xml", "html": ".html", "yaml": ".yml", "markdown": ".md", "python": ".py"}

# current_system="linux"

# 向某个进程发送crtl+c指令
def send_ctrl_c(pid):
    con.FreeConsole()
    if con.AttachConsole(int(pid)) == None:
        api.SetConsoleCtrlHandler(None, 1)
        api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
        api.Sleep(15)
        con.FreeConsole()
        api.SetConsoleCtrlHandler(None, 0)

# 通过host+port获取进程pid


def get_pid_from_port(port):
    res = os.popen(f'netstat -ano |findstr "{port}"').readlines()
    for i in res:
        if i.split()[-2] == 'LISTENING':
            print(i)
            return i.split()[-1]


def succ(data):
    return json.dumps({"code": 200, "data": data})


# 获取脚本列表
def getAllScript():
    job_list = {}
    index = 1
    for job in os.listdir(script_path):
        job_list[index] = {'name': job}
        index += 1
    current_app.logger.info(f'脚本列表：{job_list}')
    return job_list

# 执行脚本
def executeScript(task):
    if task.split('.')[1]!='.py':
        current_app.logger.info(f'{task}不是python脚本，无法执行')
        return f"非Python脚本无法执行"
    os.chdir(script_path)
    os.system(f'python {task}')
    current_app.logger.info(f'{task}执行成功')
    return f'{task}执行成功'


# 删除脚本
def deleteScript(task):
    os.chdir(script_path)
    os.system(f'del {task}')
    current_app.logger.warning(f'{task}删除成功')
    return f'{task}删除成功'

# 保存脚本


def saveScript(content, name, type):
    end = codeType[type]
    script = name + end
    with open(f'{script_path}/{script}', 'w', encoding='utf-8') as newScript:
        newScript.write(content)
    current_app.logger.info(f'{script}保存成功')
    return f'{script}保存成功'


# 读取配置文件
with open('properties.json', 'r', encoding='utf-8') as properties:
    property_dict = json.load(properties)
    config = property_dict['version']
    for i in property_dict["version"].keys():
        pass
        # from_path.append(f'{ip}{i}/')
        # to_path.append(property_dict["version"][i][0])
        # port.append(property_dict["version"][i][1])
        # ubuntu_path.append(property_dict["version"][i][2])

    root_path = property_dict["mid_path"]
YongHong_path = f'{root_path}/Yonghong'
tomcat_path = f'{root_path}/tomcat/bin/'


def is_port_used(c_ip, c_port):
    """
    check whether the port is used by other program
    检测端口是否被占用

    :param c_ip:
    :param c_port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((c_ip, c_port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def current_time():
    return time.strftime("%H:%M:%S", time.localtime())


def restart_tomcat(v):
    log = f'{current_time}<p>'
    log += shut_tomcat(v)
    log += start_tomcat(v)
    current_app.logger.info(f'{v}tomcat重启成功')
    return f'{v}tomcat重启成功！'


# 停止tomcat
def shut_tomcat(v):
    host_port = eval(config[v][1])

    if is_port_used(host_ip, host_port):
        if(current_system == "windows"):
            # if v == 'develop':
            #     print('停止trunk tomcat进程')
            os.system(f'python {script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
            # else:
            #     work_dir = config[v][0] + tomcat_path
            #     os.chdir(work_dir)
            #     os.system('shutdown')7
        else:
            work_dir = config[v][0] + tomcat_path
            os.chdir(work_dir)
            os.system('sh shutdown.sh')
        
        current_app.logger.info(f'{v}tomcat服务停止成功')
        return f'{v}tomcat服务停止成功'
    else:
        current_app.logger.info(f'{v}tomcat服务未启动')
        return f'{v}tomcat服务未启动'


def start_tomcat(v):
    # v = ip + v + '/'
    # index = from_path.index(v)
    host_port = eval(config[v][1])
    work_dir = config[v][0] + tomcat_path
    os.chdir(work_dir)
    for scape in range(100):
        if is_port_used(host_ip, host_port):
            print('tomcat正在停止中')
            time.sleep(10)
        else:
            if(current_system == "windows"):
                os.system('startup')
            else:
                os.system('sh startup.sh')
            break
    current_app.logger.info(f'启动{v}tomcat服务成功')
    return f'启动{v}tomcat服务成功'

def renameProductJar(newName,path):
    jar_list=os.listdir(path)
    for i in jar_list:
        if newName.split('.')[0] in i.split('.')[0]:
            os.rename(f'{path}/{i}',f'{path}/{newName}')

def copy_Jar(to_path_in, version):
    """
    :param
    from_path_in:源路径
    to_path_in：目标路径
    version：版本号
    index：列表中下标
    """
    if version =='v9.4.1':
        version='v9.4'
    if version == 'develop':
        from_path_in = f'{ip}{version}'
    else:
        from_path_in = f'{ip}{version}'
    log = ''
    flag = 0
    try:
        path0 = time.strftime("%Y%m%d", time.localtime())
        current_app.logger.info(f'当天的{version}jar包地址：{os.path.join(from_path_in, path0)}')
        print(f'当天的{version}jar包地址：{os.path.join(from_path_in, path0)}')
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not os.path.exists(os.path.join(from_path_in, path0)):
                year = path0[0:4]
                month = path0[4:6]
                day = path0[-2:]
                month_1 = int(month)-1
                if (month_1) > 9:
                    month_1 = str(month_1)
                else:
                    month_1 = f'0{str(month_1)}'
                if day == '01':
                    if month in day_31:
                        path0 = f'{year}{month_1}31'
                    elif month == '03' and int(year) % 4 == 0:
                        path0 = f'{year}0229'
                    elif month == '03' and int(year) % 4 != 0:
                        path0 = f'{year}0228'
                    elif month == '01':
                        path0 = f'{str(int(year) - 1)}1231'
                    else:
                        path0 = f'{year}{month_1}30'
                else:
                    path0 = str(eval(path0) - 1)
            else:
                break
        current_app.logger.info(f'最新的是{path0}的包')
        log += f'最新的是{path0}的包'
        backup_path = to_path_in + '/backup_product'
        path = os.path.join(from_path_in, path0)
        dirs = os.listdir(path)
        # 检查备份文件夹是否存在，不存在则创建
        # if not os.path.exists(backup_path):
        #     os.mkdir(backup_path)
        # backup_path += '/product' + path0
        # # 检查当天的备份文件夹，不存在则新建
        # if not os.path.exists(backup_path):
        #     os.mkdir(backup_path)
        # 遍历目标地址中的项目jar
        for file_name in dirs:
            from_file = os.path.join(path, file_name)
            to_file = os.path.join(to_path_in, "product", file_name)
            if not os.path.exists(to_file):
                renameProductJar(file_name,os.path.join(to_path_in, "product"))
            backup_file = os.path.join(backup_path, file_name)
            ubuntu_file = os.path.join(config[version][2], file_name)
            try:
                from_134_file = from_file.replace(ip, ip_134)
                if not filecmp.cmp(from_file, from_134_file):
                    from_file = from_134_file
                if not filecmp.cmp(from_file, to_file):
                    # current_app.logger.info(f'{version}有新的{file_name}\n')
                    # log += f'{version}有新的{file_name}\n'
                    # print(version + "有新的" + file_name, end='...\n')
                    # copy2(to_file, backup_file)
                    copy2(from_file, to_file)
                    copy2(from_file, ubuntu_file)
                    current_app.logger.info(f"{file_name}更新完毕,时间：{current_time()}\n")
                    log += f"{file_name}更新完毕,时间：{current_time()}\n"
                    print(f"{file_name}更新完毕,时间：{current_time()}\n")
                    flag = 1
            except PermissionError:
                current_app.logger.info(f"{path}下{file_name}正在被占用，请稍等...time{current_time()}")
                log += f"{path}下{file_name}正在被占用，请稍等...time{current_time()}"
                print(f"{path}下{file_name}正在被占用，请稍等...time{current_time()}\n")
        # if flag == 1:
        # clean_jar(to_path_in)
    except FileNotFoundError as err:
        current_app.logger.info(f'file error:{err}\n')
        log += f'\nfile error:{err}'
        print(f'\nfile error:{err}')
    return log


def copy_and_reload(v):
    """
    :param v: 版本号 develop
    :return:
    """
    log = '<p>'
    version = v
    v = ip + v + '/'
    log += f'{current_time()}</p><p>'
    # index = from_path.index(v)
    # clean_jar(to_path[index] + path)
    # 先关闭tomcat，然后换JAR，再启动tomcat
    log += shut_tomcat(version)
    log += copy_Jar(config[version][0] + YongHong_path, version)
    log += start_tomcat(version)
    return f'{log}检查完毕'


def new_copy(v):
    """
    :param v: 版本号 develop
    :return:
    """
    log = ''
    version = v
    v = ip + v + '/'
    log += f'{current_time()}'
    # index = from_path.index(v)
    # print('清理备份的jar')
    # log += '清理备份的jar'
    # clean_jar(to_path[index] + path)
    # work_dir = to_path[index] + tomcat_path
    # host_port = eval(port[index])
    # os.chdir(work_dir)
    # 先关闭tomcat，然后换JAR，再启动tomcat
    log += copy_Jar(config[version][0] + YongHong_path, version)
    current_app.logger.info(f'{v}最新包检查完毕')
    return f'{log}检查完毕'
