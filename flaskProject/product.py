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

host_ip = '127.0.0.1'
ip = '\\\\192.168.0.141/productJar/'
ip_134 = '\\\\192.168.1.134/git-package/'
from_path = []
to_path = []
day_31 = ['02', '04', '06', '08', '09', '11']
port = []
ubuntu_path = []

# 向某个进程发送crtl+c指令
def send_ctrl_c(pid):
    con.FreeConsole()
    if con.AttachConsole(int(pid)) == None:
        api.SetConsoleCtrlHandler(None, 1)
        api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
        api.Sleep(2000)
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
    for job in os.listdir(r'C:\Users\228\PycharmProjects\flaskProject\static\job'):
        job_list[index] = {'name': job}
        index += 1
    return job_list

# 执行脚本
def executeScript(task):
    os.chdir(r'C:\Users\228\PycharmProjects\flaskProject\static\job')
    os.system(f'python {task}')
    return f'{task}执行成功'


# 删除脚本
def deleteScript(task):
    os.chdir(r'C:\Users\228\PycharmProjects\flaskProject\static\job')
    os.system(f'del {task}')
    return f'{task}删除成功'

# 保存脚本
def saveScript(content, name, type):
    if type == 'python':
        script = name + '.py'
    with open('C:/Users/228/PycharmProjects/flaskProject/static/job/'+script, 'w', encoding='utf-8') as newScript:
        newScript.write(content)
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
    return f'重启成功！'


# 停止tomcat
def shut_tomcat(v):
    host_port = eval(config[v][1])

    if is_port_used(host_ip, host_port):
        if v == 'develop':
            print('停止trunk tomcat进程')
            os.system(f'python C:/Users/228/PycharmProjects/flaskProject/static/job/stopTrunk.py')
            # send_ctrl_c(get_pid_from_port(host_port))
        else:
            work_dir = config[v][0] + tomcat_path
            os.chdir(work_dir)
            os.system('shutdown')
            
        return '停止tomcat服务成功！'
    else:
        return 'tomcat服务未启动'


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
            os.system('startup')
            break
    return '启动tomcat服务成功'


def copy_Jar(to_path_in, version):
    """
    :param
    from_path_in:源路径
    to_path_in：目标路径
    version：版本号
    index：列表中下标
    """
    from_path_in = f'{ip}{version}'
    log = ''
    flag = 0
    try:
        path0 = time.strftime("%Y%m%d", time.localtime())
        print(os.path.join(from_path_in, path0))
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not os.path.exists(os.path.join(from_path_in, path0)):
                year = path0[0:4]
                month = path0[4:6]
                day = path0[-2:]
                month_1 = eval(month.replace('0',''))-1
                if (month_1) > 9:
                    month_1 = str(month_1)
                else:
                    month_1 = f'0{str(month_1)}'
                if day == '01':
                    if month in day_31:
                        path0 = f'{year}{month_1}31'
                    elif month == '03' and eval(year) % 4 == 0:
                        path0 = f'{year}0229'
                    elif month == '03' and eval(year) % 4 != 0:
                        path0 = f'{year}0228'
                    elif month == '01':
                        path0 = f'{str(eval(year) - 1)}1231'
                    else:
                        path0 = f'{year}{month_1}30'
                else:
                    path0 = str(eval(path0) - 1)
            else:
                break
        log += path0 + '的包'
        backup_path = to_path_in + '/backup_product'
        path = os.path.join(from_path_in, path0)
        dirs = os.listdir(path)
        # 检查备份文件夹是否存在，不存在则创建
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        backup_path += '/product' + path0
        # 检查当天的备份文件夹，不存在则新建
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        # 遍历目标地址中的项目jar
        for file_name in dirs:
            from_file = os.path.join(path, file_name)
            to_file = os.path.join(to_path_in, "product", file_name)
            backup_file = os.path.join(backup_path, file_name)
            ubuntu_file = os.path.join(config[version][2], file_name)
            try:
                from_134_file = from_file.replace(ip, ip_134)
                if not filecmp.cmp(from_file, from_134_file):
                    from_file = from_134_file
                if not filecmp.cmp(from_file, to_file):
                    log += version + "有新的" + file_name + '\n'
                    print(version + "有新的" + file_name, end='...\n')
                    # copy2(to_file, backup_file)
                    copy2(from_file, to_file)
                    copy2(from_file, ubuntu_file)
                    log += f"更新完毕,时间：{current_time()}\n"
                    print(f"更新完毕,时间：{current_time()}\n")
                    flag = 1
            except PermissionError:
                log += f"{path}下{file_name}正在被占用，请稍等...time{current_time()}"
                print(f"{path}下{file_name}正在被占用，请稍等...time{current_time()}\n")
        # if flag == 1:
        # clean_jar(to_path_in)
    except FileNotFoundError as err:
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
    return f'{log}检查完毕'
