import os
from filecmp import cmp, cmpfiles
from json import dump, dumps, load
import pickle
from platform import system
from shutil import copy2, copytree, rmtree
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep, localtime, strftime
from xml.dom.minidom import parse
from flask import Response
import sys
import re
from functools import wraps

from logging import getLogger
from app import if_connect_mysql

if if_connect_mysql:
    from app import db, User

product_logger = getLogger("product")

if system() == "Windows":
    import win32api as api
    import win32console as con
    from . import properties
else:
    from . import properties_Linux as properties


class ProductAction:
    current_path = r'D:\code\python\yhenv\flaskProject'
    unstable_version = ['v8.6', 'v8.7', 'v8.8', 'v9.1', 'v9.3', '9.2.1', 'v9.0']
    host_ip = '127.0.0.1'
    ip = '\\\\192.168.0.141/productJar/'
    ip_141 = '\\\\192.168.0.141/productJar/'
    ip_134 = '\\\\192.168.1.134/git-package/'
    ip_187 = '\\\\192.168.0.187/share/'
    ip_199 = '\\\\192.168.1.199'
    ip = ip_134
    from_path = []
    script_path = f"{current_path}/static/job"
    status_path = f"{current_path}/apps/productApp"
    user_info_path = f"{current_path}/apps/productApp/user.json"
    to_path = []
    day_31 = ['02', '04', '06', '08', '09', '11']
    yonghong_product_jar = ['api.jar', 'product.jar', 'thirds.jar',
                            'baidu.jar', 'base,jar', 'bi-tests.jar', 'autoNavi.jar']
    port = []
    ubuntu_path = []
    users = []
    current_system = system()
    codeType = {"default": ".py", "application/json": ".json", "sql": ".sql", "javascript": ".js", "css": ".css",
                "xml": ".xml", "html": ".html", "yaml": ".yml", "markdown": ".md", "python": ".py"}
    month_cases = ['DBPainter/res/Tab/properties/labelName__mobileDT.png',
                   'DBPainter/res/Tab/properties/labelName__mobileRT.png',
                   'DBPainter/res/Tab/properties/padding__mobileDT.png',
                   'DBPainter/res/Tab/properties/padding__mobileRT.png',
                   'DBPainter/res/Tab/properties/padding__日期过滤1__RT.png',
                   'DBPainter/res/Tab/properties/padding__选项卡6__RT.png',
                   'DBPainter/res/Tab/properties/positionType__mobileDT.png',
                   'DBPainter/res/Tab/properties/positionType__mobileRT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤1__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤2__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤3__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤4__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤5__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤6__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤7__RT.png',
                   'DBPainter/res/Tab/properties/positionType__日期过滤8__RT.png',
                   'DBPainter/res/Carousel/elemsFilt.pdf', 'DBPainter/res/Carousel/elemsFilt__mobileDT.png',
                   'Export/res/Export/cbug/YH-CIssue-09385__Properties2.png',
                   'DBPainter/res/Carousel/elemsFilt__mobileRT.png']
    root_path = ''
    YongHong_path = ''
    vividime_path = ''
    tomcat_path = ''
    bi_xml_path = ''
    server_xml_path = ''
    config = {}
    jar_list = {}
    release_jar_list = {}
    status = {}
    jobs = []

    # current_system="linux"
    def __init__(self) -> None:

        self.read_config()
        if if_connect_mysql:
            self.users = User.query.filter().all()
            with open(f'{self.status_path}/allusers.user', 'wb') as users:
                pickle.dump(self.users, users)
        else:
            with open(f'{self.status_path}/allusers.user', 'rb') as users:
                self.users = pickle.load(users)
        if self.current_system == "Windows":
            self.jar_list = self.get_jar_list()
            self.release_jar_list = self.get_release_jar_list()

    # 删除字符串内特殊字符  
    @staticmethod
    def delete_boring_characters(sentence=""):

        return re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", sentence)

    # 向某个进程发送crtl+c指令
    @staticmethod
    def send_ctrl_c(pid):
        con.FreeConsole()
        if con.AttachConsole(int(pid)) is None:
            api.SetConsoleCtrlHandler(None, 1)
            api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
            api.Sleep(15)
            con.FreeConsole()
            api.SetConsoleCtrlHandler(None, 0)

    @staticmethod
    def clear_list_not_num(array=None):
        """
        :param array: 日期列表
        :return:清空非纯数字的子项
        """
        if array is None:
            return []
        new_array = [i for i in array if i.isdigit()]
        # for i in array:
        #     if i.isdigit():
        #         new_array.append(i)
        return new_array

    @staticmethod
    def format_date_str(date_str=''):
        """
        :param date_str:日期字符串
        :return:返回格式化后的字符串
        """
        if date_str == '':
            return date_str
        return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"

    @staticmethod
    def clear_list_dumplicate(array=None):
        return list(set(array))

    # 通过host+port获取进程pid
    def get_pid_by_port(self, port):
        res = self.readlines_command(f'netstat -ano |findstr "{port}"')
        for i in res:
            if i.split()[-2] == 'LISTENING':
                product_logger.info(i)
                return i.split()[-1]

    @staticmethod
    def succ(data=""):
        return Response(dumps({"code": 200, "data": data}, ensure_ascii=False, separators=(',', ':')),
                        mimetype='application/json')

    @staticmethod
    def error(data=""):
        return Response(dumps({"code": 500, "data": data}, ensure_ascii=False, separators=(',', ':')),
                        mimetype='application/json')

    @staticmethod
    def user_not_found(user):
        return Response(dumps({"code": 405, "data": f"{user}用户不存在"}, ensure_ascii=False, separators=(',', ':')),
                        mimetype='application/json')

    @staticmethod
    def info(data=""):
        return Response(dumps({"code": 205, "data": data}, ensure_ascii=False, separators=(',', ':')),
                        mimetype='application/json')

    # 获取脚本列表
    def get_all_script(self):
        job_list = {}
        index = 1
        for job in os.listdir(self.script_path):
            job_list[index] = {'name': job}
            index += 1
        product_logger.info(f'脚本列表：{job_list}')
        return job_list

    # 执行脚本
    def execute_script(self, task):
        if task.split('.')[1] != '.py':
            product_logger.info(f'{task}不是python脚本，无法执行')
            return f"非Python脚本无法执行"
        os.chdir(self.script_path)
        self.read_command(f'python {task}')
        product_logger.info(f'{task}执行成功')
        return f'{task}执行成功'

    # 删除脚本
    def delete_script(self, task):
        os.chdir(self.script_path)
        self.read_command(f'del {task}')
        product_logger.warning(f'{task}删除成功')
        return f'{task}删除成功'

    # 保存脚本
    def save_script(self, content, name, type):
        end = self.codeType[type]
        script = name + end
        with open(f'{self.script_path}/{script}', 'w', encoding='utf-8') as newScript:
            newScript.write(content)
        product_logger.info(f'{script}保存成功')
        return f'{script}保存成功'

    def init_config(self, key):
        self.config[key]["port"], self.config[key]["closePort"] = self.get_bi_port(key)
        self.config[key]["bihome"] = self.get_bi_home(key)
        if 'dis' in key:
            self.config[key]['url'] = self.config[key]["port"] + \
                                      '/bi/?showOthers=true'
        else:
            self.config[key]['url'] = self.config[key]["port"] + '/bi'
        self.config[key]["debug"] = self.get_debug_port(key)
        self.config[key]["startup"] = False
        self.config[key]["shutdown"] = False
        self.config[key]["update"] = False
        self.config[key]["reload"] = False
        self.config[key]["updateAndReload"] = False
        self.config[key]["changeBihome"] = False
        self.config[key]["status"] = '1' if self.is_port_used_fast(
            self.config[key]["port"]) else '0'
        if "yh" in self.config[key].keys():
            current_jar_path_info = os.path.join(self.config[key]["path"] + self.vividime_path, "product",
                                                 "currentPath.txt")
            bi_pro_path = os.path.join(self.config[key]["path"] + self.vividime_path, self.config[key]["bihome"],
                                       'bi.properties')
        else:
            current_jar_path_info = os.path.join(self.config[key]["path"] + self.YongHong_path, "product",
                                                 "currentPath.txt")
            bi_pro_path = os.path.join(self.config[key]["path"] + self.YongHong_path, self.config[key]["bihome"],
                                       'bi.properties')
        if os.path.exists(current_jar_path_info):
            with open(current_jar_path_info, 'r', encoding='utf-8') as path_info:
                self.config[key]["currentJarPath"] = path_info.read()
        else:
            self.config[key]["currentJarPath"] = ''
        if os.path.exists(bi_pro_path):
            self.config[key]["biProPath"] = bi_pro_path
        else:
            self.config[key]["biProPath"] = ''

    # 读取配置文件
    def read_config(self):
        self.config = properties.env_list['version']
        self.root_path = properties.env_list["mid_path"]
        self.YongHong_path = f'{self.root_path}/Yonghong'
        self.vividime_path = f'{self.root_path}/vividime'
        self.tomcat_path = f'{self.root_path}/tomcat/bin/'
        self.bi_xml_path = f'{self.root_path}/tomcat/webapps/bi/WEB-INF/web.xml'
        self.server_xml_path = f'{self.root_path}/tomcat/conf/server.xml'
        for key in self.config.keys():
            self.init_config(key)
        self.update_product_status()
        # with open(f'{self.current_path}/apps/productApp/user.json', 'r', encoding='utf-8') as user:
        #     self.users = load(user)

    def update_config(self):
        for key in properties.env_list['version'].keys():
            if key not in self.config.keys():
                continue
            self.init_config(key)
        self.update_product_status()

    def get_debug_port(self, version):
        if self.current_system == "Windows":
            catalina_path = f'{self.config[version]["path"]}{self.tomcat_path}catalina.bat'
        else:
            catalina_path = f'{self.config[version]["path"]}{self.tomcat_path}catalina.sh'
        with open(catalina_path, 'r', encoding='utf-8') as catalina:
            catalina_lines = catalina.readlines()
            for i in catalina_lines:
                if 'set JPDA_ADDRESS=' in i and 'if not "%JPDA_ADDRESS%" == "" goto gotJpdaAddress' not in \
                        catalina_lines[catalina_lines.index(i) - 1]:
                    return i.split('=')[1].split(':')[1][0:-1]
        return "未配置"

    @staticmethod
    def update_file(file, old_str, new_str):
        """
        替换文件中的字符串
        :param file:文件名
        :param old_str:旧字符串
        :param new_str:新字符串
        :return:
        """
        file_data = ""
        with open(file, "r") as f:
            for line in f:
                line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w") as f:
            f.write(file_data)

    def change_bi_home(self, version, bihome):
        split_str = '\\' if self.current_system == "Windows" else '/'
        reload = False
        if self.is_port_used('localhost', eval(self.config[version]["port"])):
            reload = True
        if reload:
            self.shut_tomcat(version)
        web_xml_file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        self.update_file(web_xml_file_path, self.config[version]['bihome'], bihome)
        if reload:
            self.start_tomcat(version)
        c_bihome = self.get_bi_home(version)
        if c_bihome != bihome:
            product_logger.info(f"bihome 修改为{bihome}失败")
            return "bihome修改失败"
        else:
            self.config[version]['bihome'] = bihome
            product_logger.info(f"bihome 修改为{bihome}成功")
            return "bihome修改成功"

    def get_bi_home(self, version):
        try:
            if self.current_system == "Windows":
                split_str = '\\'
            else:
                split_str = '/'
            file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
            dom = parse(file_path)
            root = dom.documentElement
            param = root.getElementsByTagName('param-value')
            entry = root.getElementsByTagName('env-entry-value')
            param_value = param[0].firstChild.data.split(split_str)
            entry_value = entry[0].firstChild.data.split(split_str)
            if param_value[-1] == entry_value[-1]:
                return param_value[-1]
        except IndexError:
            return "error bihome"
            pass
        except:
            return "error bihome"
            product_logger.error(f"Unexpected error:{sys.exc_info()[0]}")

    def get_bi_port(self, version):
        file_path = f'{self.config[version]["path"]}{self.server_xml_path}'
        dom = parse(file_path)
        root = dom.documentElement
        connect = root.getElementsByTagName('Connector')
        server = root.getElementsByTagName('Server')
        start_port = connect[0].getAttribute('port')
        shutdown_port = root.getAttribute('port')
        return start_port, shutdown_port

    @staticmethod
    def is_port_used(c_ip, c_port):
        """
        check whether the port is used by other program
        检测端口是否被占用
        :param c_ip:
        :param c_port:
        :return:
        """
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((c_ip, c_port))
            return True
        except OSError:
            return False
        finally:
            s.close()

    @staticmethod
    def read_command(cmd):
        with os.popen(cmd) as p:
            res = p.read()
        return res

    @staticmethod
    def readlines_command(cmd):
        with os.popen(cmd) as p:
            res = p.readlines()
        return res

    def is_port_used_fast(self, c_port):
        cmd = f'netstat -ano |findstr {c_port}'
        res = self.read_command(cmd)
        if "LISTENING" in res or "LISTEN" in res:
            return True
        return False

    def get_bind_port(self, ports):
        bind_ports = []
        for port in ports:
            if self.is_port_used_fast(port):
                bind_ports.append(port)
        return bind_ports

    @staticmethod
    def current_time():
        return strftime("%H:%M:%S", localtime())

    def restart_tomcat(self, v, user=''):
        if self.config[v]['reload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        if self.config[v]['updateAndReload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境并更换jar包，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        self.change_status(v, 'reload', True)
        self.shut_tomcat(v)
        self.start_tomcat(v, user)
        product_logger.info(f'[user]-{v} tomcat重启成功')
        self.change_status(v, 'reload')
        return f'{v} tomcat重启成功！'

    @staticmethod
    def get_pid_by_port_linux(port):
        with os.popen(f'lsof -i:{port}') as p:
            res = p.readlines()
        res.pop(0)
        pid = [i.split()[1] for i in res]
        # for i in res:
        #     pid.append(i.split()[1])
        return ','.join(set(pid))

    # 停止tomcat
    def shut_tomcat(self, v):
        check_res = self.check_status(v)
        if check_res != '0':
            return check_res
        self.change_status(v, 'shutdown', True)
        host_port = eval(self.config[v]["port"])
        ports = [self.config[v]["port"], self.config[v]["closePort"]]
        bind_ports = self.get_bind_port(ports)
        product_logger.info(f'停止{v} 已绑定的端口-{bind_ports}')
        if bind_ports:
            if self.current_system == "Windows":
                product_logger.info(f'停止{v} tomcat进程')
                for port in bind_ports:
                    if v == 'trunk':
                        self.read_command(
                            f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
                    else:
                        self.read_command(f"taskkill /f /pid {self.get_pid_by_port(eval(port))}")
            else:
                work_dir = self.config[v]["path"] + self.tomcat_path
                os.chdir(work_dir)
                product_logger.info(f'进入目录{work_dir}')
                product_logger.info(f'执行命令：sh {work_dir}shutdown.sh')
                self.read_command(f'sh {work_dir}shutdown.sh')
            while 1:
                if self.get_bind_port(ports):
                    product_logger.info(f'{v} tomcat服务停止中')
                else:
                    product_logger.info(f'{v} tomcat服务停止成功')
                    break
                sleep(2)
            self.config[v]["status"] = '0'
            self.change_status(v, 'shutdown')
            return f'{v} tomcat服务停止成功'
        else:
            self.config[v]["status"] = '0'
            self.change_status(v, 'shutdown')
            product_logger.info(f'{v} tomcat服务未启动')
            return f'{v} tomcat服务未启动'

    def start_tomcat(self, v, user=''):
        check_res = self.check_status(v)
        if check_res != '0':
            return check_res
        self.change_status(v, 'start', True)
        host_port = eval(self.config[v]["port"])
        work_dir = self.config[v]["path"] + self.tomcat_path
        os.chdir(work_dir)
        # product_logger.info(self.read_command('pwd'))
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.config[v]["status"] != '0':
                    product_logger.info(f'已启动{v} tomcat服务')
                    self.config[v]["status"] = '1'
                    self.change_status(v, 'start')
                    return f'已启动{v} tomcat服务'
                else:
                    sleep(10)
                    product_logger.info('tomcat正在停止中')
            else:
                if self.current_system == "Windows":
                    if self.config[v]["debug"].isdigit():
                        os.system('catalina.bat jpda start > NUL')
                    else:
                        os.system('startup > NUL')
                else:
                    self.read_command('sh startup.sh > caches.txt')
                break
        product_logger.info(f'启动{v} tomcat服务成功')
        self.config[v]["status"] = '1'
        self.change_status(v, 'start')
        return f'启动{v} tomcat服务成功'

    @staticmethod
    def rename_product_jar(new_name, path):
        jar_list = os.listdir(path)
        for i in jar_list:
            if i.split('.')[0] == 'product-swf':
                os.rename(f'{path}/{i}', f'{path}/product-swf.jar')
            elif new_name.split('.')[0] in i.split('.')[0]:
                os.rename(f'{path}/{i}', f'{path}/{new_name}')

    def get_recent_jar(self, version):
        branch = self.config[version]["branch"]
        from_path_in = f'{self.ip}{branch}'
        path0 = strftime("%Y%m%d", localtime())
        product_logger.info(
            f'当天的{version}jar包地址：{os.path.join(from_path_in, path0)}')
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not os.path.exists(os.path.join(from_path_in, path0)):
                year = path0[0:4]
                month = path0[4:6]
                day = path0[-2:]
                month_1 = int(month) - 1
                month_1 = str(month_1) if month_1 > 9 else f'0{str(month_1)}'
                if day == '01':
                    if month in self.day_31:
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
        product_logger.info(f'最新的是{path0}的包')
        return os.path.join(from_path_in, path0)

    def get_fast_path(self, version, date=strftime("%Y%m%d", localtime())):
        git_branch = self.config[version]["branch"]
        path_187 = f'{self.ip_187}{git_branch}/{date}'
        path_134 = f'{self.ip}{git_branch}/{date}'
        if not os.path.exists(path_187) and not os.path.exists(path_134):
            product_logger.info(f'[system] {version}没有新的jar包')
            return ''
        common = ['api.jar', 'product.jar', 'thirds.jar']
        if os.path.exists(path_187) and os.path.exists(path_134):
            mismatch = cmpfiles(path_134, path_187, common)[1]
            if not mismatch:
                return path_187
            return path_187
            # return path_134
        return path_187 if os.path.exists(path_187) else path_134

    def if_copy_custom(self, v, custom_path):
        if_update = False
        if custom_path:
            custom_path_187 = self.ip_187 + custom_path
            custom_path_141 = self.ip_141 + custom_path
            custom_path_134 = self.ip_134 + custom_path
            custom_full_path = [custom_path_187, custom_path_141, custom_path_134]
            for path in custom_full_path:
                if os.path.exists(path):
                    self.copy_custom_jar(v, path)
                    if_update = True
                    break
                product_logger.info(f'{v}-{custom_path} jar包不存在')
        return if_update

    def new_copy(self, v, date='', copy_release=False, release='', custom_path=''):
        """
        复制jar包api
        :param custom_path: 自定义换包路径
        :param v: 版本
        :param date: 日期
        :param copy_release: 是否复制release
        :param release: 发布版本
        :return:
        """
        if_update = False
        if custom_path:
            if_update = self.if_copy_custom(v, custom_path)
        if not if_update:
            self.copy_jar(v, date) if not copy_release else self.copy_release_jar(v, release)
        product_logger.info(f'{v}-{self.format_date_str(date)} jar包检查完毕')
        self.change_status(v, 'update')
        return f'{v}已更换{self.format_date_str(date)} jar包'

    def copy_jar(self, version, date):
        """
        :param version: 版本号
        :param date: jar包日期
        :return:
        :param
        from_path_in:源路径
        to_path_in：目标路径
        version：版本号
        """
        try:
            check_res = self.check_status(version)
            if check_res != '0':
                return check_res
            self.change_status(version, 'update', True)
            if "yh" in self.config[version].keys():
                to_path_in = self.config[version]["path"] + self.vividime_path
            else:
                to_path_in = self.config[version]["path"] + self.YongHong_path
            local_jar_path = os.path.join(to_path_in, "product")
            branch = self.config[version]["branch"]
            date_jar_path = self.get_fast_path(version, date)
            if date_jar_path == "" or date == "":
                self.change_status(version, "update")
                return f"{version}没有{'新' if date == '' else date}的jar包"
            dirs = os.listdir(date_jar_path)
            res = self.cycle_copy(date_jar_path, local_jar_path, version)
            log_info = f'{version}-{self.format_date_str(date)} Jar包更新完成' if res == 1 else res
        except FileNotFoundError as err:
            self.change_status(version, 'update')
            log_info = f'file error:{err}'
        product_logger.info(log_info)
        self.change_status(version, 'update')
        return log_info

    def copy_release_jar(self, version, release_version):
        """
        :param version: 环境的key
        :param release_version: release的版本
        :return:
        """
        product_logger.info(f'release version:{release_version}')
        if os.path.exists(f'{self.ip_187}common/{release_version}'):
            release_jar_path = f'{self.ip_187}common/{release_version}'
        else:
            release_jar_path = f'{self.ip_134}common/{release_version}'
        if "yh" in self.config[version].keys():
            local_jar_path = os.path.join(self.config[version]["path"] + self.vividime_path, "product")
        else:
            local_jar_path = os.path.join(self.config[version]["path"] + self.YongHong_path, "product")
        res = self.cycle_copy(release_jar_path, local_jar_path, version)
        log_info = f'{version}-{release_version} Jar包更新完成' if res == 1 else res
        product_logger.info(log_info)
        self.change_status(version, 'update')
        return log_info

    def copy_custom_jar(self, version, custom_path):
        product_logger.info(f'custom path:{custom_path}')
        if "yh" in self.config[version].keys():
            local_jar_path = os.path.join(self.config[version]["path"] + self.vividime_path, "product")
        else:
            local_jar_path = os.path.join(self.config[version]["path"] + self.YongHong_path, "product")
        res = self.cycle_copy(custom_path, local_jar_path, version)
        log_info = f'{version}-{custom_path} Jar包更新完成' if res == 1 else res
        product_logger.info(log_info)
        self.change_status(version, 'update')
        return log_info

    @staticmethod
    def verbose_copy(src, dst):
        if src.endswith(".jar"):
            return copy2(src, dst)

    @staticmethod
    def ignore_func(dir, files):
        # 忽略所有以“vooltdb”开头的目录和文件
        return [f for f in files if f.startswith('vooltdb')]

    def cycle_copy(self, src, dst, version):
        """
        循环复制整个目录jar包
        :param src: 源文件夹
        :param dist: 目标文件夹
        :param version: 版本
        :return:
        """
        max_count = 0
        while True:
            try:
                if os.path.exists(dst):
                    product_logger.info(f'delete folder:{dst}')
                    rmtree(dst)  # 先删除原本的
                    product_logger.info(f'copy:{src} to {dst}')
                    copytree(src, dst, ignore=self.ignore_func, copy_function=self.verbose_copy)  # 整个复制过来
                    os.system(f'echo {src} > {dst}/currentPath.txt')
                    self.config[version]["currentJarPath"] = src
                    return 1
            except PermissionError:
                if max_count > 10:
                    self.change_status(version, 'update')
                    log_info = f"{dst}下文件正在被占用，请稍等...time{self.current_time()}"
                    product_logger.info(log_info)
                    return log_info
                max_count += 1
                product_logger.info(
                    f"{dst}下文件正在被占用，请稍等...time{self.current_time()}")
                sleep(10)

    def copy_and_reload(self, v, date, user='', copy_release=False, release='', custom_path=''):
        """
        :param custom_path:
        :param v: 版本
        :param date: jar包日期
        :param user: 用户
        :param copy_release: 是否复制release的jar包
        :param release: release版本
        :return:
        """
        res = ""
        if self.config[v]['updateAndReload']:
            res = f'正在重启{v}环境并更换jar包，请稍等'
            product_logger.info(res)
            return res
        if self.config[v]['reload']:
            res = f'正在重启{v}环境，请稍等'
            product_logger.info(res)
            return res
        self.change_status(v, "updateAndReload", True)
        self.shut_tomcat(v)
        if_update = False
        if custom_path:
            if_update = self.if_copy_custom(v, custom_path)
        if not if_update:
            res = self.copy_jar(v, date) if not copy_release else self.copy_release_jar(v, release)
        self.change_status(v, "updateAndReload", True)
        # 先关闭tomcat，然后换JAR，再启动tomcat
        self.start_tomcat(v, user)
        self.config[v]["startUser"] = user
        self.change_status(v, "updateAndReload")
        if "没有" not in res:
            return f'{v}已更换{self.format_date_str(date)} jar包并重启Tomcat成功'
        return res

    def get_jar_info(self, v):
        if "yh" in self.config[v].keys():
            product_path = os.path.join(self.config[v]["path"] + self.vividime_path, 'product')
        else:
            product_path = os.path.join(self.config[v]["path"] + self.YongHong_path, 'product')
        info_list = [f'当前的jar包路径：{self.config[v]["currentJarPath"]}'] if self.config[v]["currentJarPath"] else []
        for i in os.listdir(product_path):
            if 'currentPath' in i:
                continue
            change_time = strftime("日期:%Y%m%d 时间:%H:%M:%S",
                                   localtime(os.stat(os.path.join(product_path, i)).st_mtime))
            info_list.append(f"{i}:{change_time}")
        return info_list

    def get_jar_list(self):
        jar_list = {}
        for key in self.config.keys():
            branch = self.config[key]["branch"]
            dir_187 = os.listdir(f'{self.ip_187}{branch}') if os.path.exists(
                f'{self.ip_187}{branch}') else []
            if os.path.exists(f'{self.ip_134}{branch}'):
                try:
                    dir_134 = os.listdir(f'{self.ip_134}{branch}') if os.path.exists(f'{self.ip_134}{branch}') else []
                    dir_187.extend(dir_134)
                except FileNotFoundError:
                    product_logger.info(f"{key}--134服务器暂时无法连接")
            dir_list = self.clear_list_dumplicate(dir_187)
            jar_list[key] = dir_list
            jar_list[key] = self.clear_list_not_num(jar_list[key])
            jar_list[key].sort()
            jar_list[key].reverse()
        return jar_list

    def get_release_jar_list(self):
        """
        获取release的jar包列表
        :return:
        """
        jar_list = {}
        exclude = ['9.2']
        release_jar_path = f'{self.ip_187}common' if os.path.exists(f'{self.ip_187}common') else f'{self.ip_134}common'
        for key in self.config.keys():
            branch = self.config[key]["branch"]
            jar_list[key] = []
            if 'custom' in branch or branch == 'develop':
                continue
            if branch.replace('v', '') in exclude:
                continue
            branch_fmt_list = branch.replace('v', '').split('.')
            branch_fmt = f'{branch_fmt_list[0]}.{branch_fmt_list[1]}'
            try:
                for release in os.listdir(release_jar_path):
                    if release in exclude or release == '9.4':
                        continue
                    if branch_fmt in release:
                        jar_list[key].append(release)
            except FileNotFoundError as file_not_found:
                jar_list[key].append(f'file not found:{file_not_found}')
        return jar_list

    def get_bi_properties(self, v):
        bi_pro = {'version': v, 'data': []}
        with open(self.config[v]['biProPath'], 'r', encoding='utf-8') as biPro:
            for param in biPro.read().splitlines():
                if not param.startswith('#'):
                    bi_pro['data'].append({'key': param.split('=')[0], 'value': param.split('=')[1]})
        return bi_pro

    def input_to_bi_properties(self, v, bipro):
        with open(self.config[v]['biProPath'], 'w', encoding='utf-8') as bi_properties:
            bi_properties.write('\n'.join(bipro))

    def modify_bi_properties(self, v, bipro, user=''):
        bi_pro = []
        bi_pro_dict = {}
        o_properties = []
        o_properties_dict = {}
        with open(self.config[v]['biProPath'], 'r', encoding='utf-8') as biPro:
            for param in biPro.read().splitlines():
                if not param.startswith('#'):
                    # o_properties.append(param)
                    o_properties_dict[param.split("=")[0]] = param.split("=")[1]
        for param in bipro:
            bi_pro_dict[param["key"]] = param["value"]
            # bi_pro_dict.append({param["key"]: param["value"]})
            bi_pro.append(f'{param["key"]}={param["value"]}')
        added = {k: bi_pro_dict[k] for k in bi_pro_dict if k not in o_properties_dict}
        removed = {k: o_properties_dict[k] for k in o_properties_dict if k not in bi_pro_dict}
        modified = {k: f'{o_properties_dict[k]}---->{bi_pro_dict[k]}' for k in bi_pro_dict if k in o_properties_dict and o_properties_dict[k] != bi_pro_dict[k]}
        if added or removed or modified:
            product_logger.info(f'version:{v},user-[{user}],新增属性:{added},删除属性:{removed},修改属性:{modified}')
            self.input_to_bi_properties(v, bi_pro)
            return 'bi.properties修改成功'
        # if len(o_properties) != len(bi_pro):
        #     product_logger.info(f'version:{v},old_properties:{o_properties},new:{bi_pro}')
        #     self.input_to_bi_properties(v, bi_pro)
        #     return 'bi.properties修改成功'
        # for pro in bi_pro:
        #     if pro not in o_properties:
        #         product_logger.info(f'version:{v},old_properties:{o_properties_dict[pro.split("=")[0]]},new:{pro}')
        #         self.input_to_bi_properties(v, bi_pro)
        #         return 'bi.properties修改成功'
        return 'bi.properties没有变化'

    def check_status(self, v, user=''):
        status = self.config[v]
        if status['startup']:
            res = f'已启动{v}环境，请刷新'
        elif status['shutdown']:
            res = f'正在关闭{v}环境，请稍等'
        elif status['update']:
            res = f'正在更新{v}环境jar包，请稍等'
        elif status['changeBihome']:
            res = f'正在更换{v}bihome路径，请稍等'
        else:
            res = '0'
        if res != '0':
            product_logger.info(res)
        return res

    def change_status(self, v, key, flag=False):
        self.config[v][key] = flag
        self.update_product_status()

    def update_product_status(self):
        with open(f'{self.status_path}/status.json', 'w', encoding='utf-8') as status:
            dump(self.config, status, indent=4, ensure_ascii=False)

    def change_junit_exp(self, case_list):
        branchs = {'branch/v8.6': 'v8.6_test', 'branch/v9.0': 'v9.0_test',
                   'branch/v9.2.1': 'v9.2.1_test', 'branch/v9.4': 'v9.4_test', 'trunk': 'trunk_test'}
        module = case_list['module']
        local_path = r'D:\SVN'
        version = case_list['version']
        cases = case_list['cases']
        testcase = r"assetExecute/testcases"
        for local, remote in branchs.items():
            if version not in remote:
                continue
            patha = os.path.join(self.ip_199, remote, testcase, module, 'res')
            pathb = os.path.join(local_path, local, 'test',
                                 testcase, module, 'exp')
            os.chdir(pathb)
            self.read_command('svn cleanup')
            res = self.read_command('svn update')
            product_logger.info(res)
            for case in cases:
                dos = f'copy "{patha}/{case}*" "{pathb}/{"/".join(case.split("/")[0:-1])}"'
                product_logger.info(dos)
                res = self.read_command(dos)
                product_logger.info(res)
        # with open(f'{self.status_path}/cases.json', 'w', encoding='utf-8') as cases:
        #     dump(case_list, cases, indent=4, ensure_ascii=False)

    def user_validation(self, userinfo):
        username = userinfo['username']
        passwd = userinfo['password']
        user = self.get_user_by_username(username)
        if user:
            return self.succ("登录成功") if passwd == user.password else self.info("密码错误")
        return self.info("用户不存在")

    def get_user_by_username(self, username):
        username = self.delete_boring_characters(username)
        for user in self.users:
            all_usersnames = f'{user.username},{user.alias}'
            if username.strip().lower() in all_usersnames:
                return user
        return ""

    def update_userlist(self):
        self.users = User.query.filter().all()

    def update_userinfo(self, userinfo):
        if not if_connect_mysql:
            return self.info("数据库暂时无法连接")
        username = userinfo["username"].strip().lower()
        password = userinfo["password"]
        alias = userinfo["alias"].strip().lower()
        email = userinfo["email"]
        user = User.query.filter(User.username == username).first()
        if user:
            change = (user.username != username) | (user.password != password) | (
                    user.alias != alias) | (user.email != email)
            if change:
                user.username = username
                user.password = password
                user.alias = alias
                user.email = email
                db.session.commit()
                self.update_userlist()
                return self.succ("用户信息修改成功")
            return self.info("用户信息无变化")
        return self.info("用户不存在")

    def create_new_user(self, userinfo):
        if not if_connect_mysql:
            return self.info("数据库暂时无法连接")
        username = userinfo["username"].strip().lower()
        password = userinfo["password"]
        alias = userinfo["alias"].strip().lower()
        email = userinfo["email"]
        if not User.query.filter(User.username == username).first():
            user = User(username, password, alias, email)
            db.session.add(user)
            # 连接数据库，添加进MySQL中
            db.session.commit()
            self.update_userlist()
            return self.succ("用户添加成功")
        return self.info("用户已存在")

    def delete_user(self, username):
        if not if_connect_mysql:
            return self.info("数据库暂时无法连接")
        user = User.query.filter(User.username == username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            self.update_userlist()
            return self.succ("用户删除成功")
        return self.info("用户不存在")

    def exchange_junit_exp(self, data, exp_folder='exp'):
        # data = loads(request.get_data())
        exp_path = f'D:\\share\\junit_test\\{data["version"]}_test\\assetExecute\\testcases'
        update_suite = []
        for case in data["cases"]:
            case_name = case.split('/')[-1]
            suite = case.split('/')[0]
            src = f'{exp_path}\\' + case.replace("/", "\\")
            if suite not in update_suite:
                res = self.read_command(f'svn up {os.path.join(exp_path, suite, "exp")}')
                if len(res.split('\n')) != 3:
                    product_logger.info(res)
                update_suite.append(suite)
            # src = os.path.join(exp_path, case)
            if not os.path.exists(src):
                product_logger.info(f'{src}文件不存在，跳过')
                continue
            dst = src.replace('res', exp_folder)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    rmtree(dst)
                    product_logger.info(f'{dst}文件夹删除后再更新')
                copytree(src, dst)
            else:
                if not os.path.exists(dst):
                    product_logger.info(f'{dst}文件不存在，直接copy')
                    dst = dst.replace(f'\\{case_name}', '')
                    if not os.path.exists(dst):
                        product_logger.info(f'{dst}文件夹不存在，需要先创建文件夹')
                        os.system(f'mkdir -p {dst}')
                copy2(src, dst)
        product_logger.info(f'[{data["user"]}]-{data["cases"]} exchanged')
        return self.succ("更换成功")

    def get_all_schedule(self):
        with open('personal-schedule.json', 'r', encoding='utf-8') as jobs:
            personal_jobs = load(jobs)
            self.jobs.extend(personal_jobs)

    @staticmethod
    def transToWinPath(path):
        pass
