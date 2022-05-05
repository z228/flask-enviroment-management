# from _typeshed import Self
import imp
import os
import time
from shutil import copy2, rmtree
import filecmp
import socket
import json
from flask import current_app
import xml.dom.minidom
# from .status import toked
import platform
import _thread

from apps.productApp import status

if platform.system() == "Windows":
    import win32api as api
    import win32console as con
    from . import properties
else:
    from . import properties_Linux as properties


class ProductAction:
    host_ip = '127.0.0.1'
    ip = '\\\\192.168.0.141/productJar/'
    ip_134 = '\\\\192.168.1.134/git-package/'
    ip_187 = '\\\\192.168.0.187/share/'
    ip = ip_134
    from_path = []
    script_path = f"{os.getcwd()}/static/job"
    status_path = f"{os.getcwd()}/apps/productApp/status.json"
    to_path = []
    day_31 = ['02', '04', '06', '08', '09', '11']
    port = []
    ubuntu_path = []
    current_system = platform.system()
    codeType = {"default": ".py", "application/json": ".json", "sql": ".sql", "javascript": ".js", "css": ".css",
                "xml": ".xml", "html": ".html", "yaml": ".yml", "markdown": ".md", "python": ".py"}
    root_path = ''
    YongHong_path = ''
    tomcat_path = ''
    bi_xml_path = ''
    server_xml_path = ''
    config = {}
    jar_list = {}
    status = {}

    # current_system="linux"
    def __init__(self) -> None:
        self.read_config()
        if self.current_system == "Windows":
            self.jar_list = self.get_jar_list()

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
            array = []
        new_array = []
        for i in array:
            if i.isdigit():
                new_array.append(i)
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

    # 通过host+port获取进程pid
    @staticmethod
    def get_pid_from_port(port):
        res = os.popen(f'netstat -ano |findstr "{port}"').readlines()
        for i in res:
            if i.split()[-2] == 'LISTENING':
                current_app.logger.info(i)
                return i.split()[-1]

    @staticmethod
    def succ(data):
        return json.dumps({"code": 200, "data": data})

    @staticmethod
    def info(data):
        return json.dumps({"code": 205, "data": data})

    # 获取脚本列表
    def get_all_script(self):
        job_list = {}
        index = 1
        for job in os.listdir(self.script_path):
            job_list[index] = {'name': job}
            index += 1
        current_app.logger.info(f'脚本列表：{job_list}')
        return job_list

    # 执行脚本
    def execute_script(self, task):
        if task.split('.')[1] != '.py':
            current_app.logger.info(f'{task}不是python脚本，无法执行')
            return f"非Python脚本无法执行"
        os.chdir(self.script_path)
        os.system(f'python {task}')
        current_app.logger.info(f'{task}执行成功')
        return f'{task}执行成功'

    # 删除脚本
    def delete_script(self, task):
        os.chdir(self.script_path)
        os.system(f'del {task}')
        current_app.logger.warning(f'{task}删除成功')
        return f'{task}删除成功'

    # 保存脚本
    def save_script(self, content, name, type):
        end = self.codeType[type]
        script = name + end
        with open(f'{self.script_path}/{script}', 'w', encoding='utf-8') as newScript:
            newScript.write(content)
        current_app.logger.info(f'{script}保存成功')
        return f'{script}保存成功'

    # 读取配置文件
    def read_config(self):
        self.config = properties.env_list['version']
        self.root_path = properties.env_list["mid_path"]
        self.YongHong_path = f'{self.root_path}/Yonghong'
        self.tomcat_path = f'{self.root_path}/tomcat/bin/'
        self.bi_xml_path = f'{self.root_path}/tomcat/webapps/bi/WEB-INF/web.xml'
        self.server_xml_path = f'{self.root_path}/tomcat/conf/server.xml'
        for key in self.config.keys():
            self.config[key]["port"] = self.get_bi_port(key)
            self.config[key]["bihome"] = self.get_bi_home(key)
            if 'dis' in key:
                self.config[key]['url'] = self.config[key]["port"] + '/bi/?showOthers=true'
            else:
                self.config[key]['url'] = self.config[key]["port"] + '/bi'
            self.config[key]["debug"] = self.get_debug_port(key)
            self.config[key]["startup"] = False
            self.config[key]["shutdown"] = False
            self.config[key]["update"] = False
            self.config[key]["reload"] = False
            self.config[key]["updateAndReload"] = False
            self.config[key]["changeBihome"] = False
            self.config[key]["status"] = '1' if self.is_port_used_fast(self.config[key]["port"]) else '0'
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

    def change_bi_home(self, version, bihome):
        split_str = '\\' if self.current_system == "Windows" else '/'
        reload = False
        if self.is_port_used('localhost', eval(self.config[version]["port"])):
            reload = True
        if reload:
            self.shut_tomcat(version)
        web_xml_file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        dom = xml.dom.minidom.parse(web_xml_file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        param_value[-1] = bihome
        entry_value[-1] = bihome
        self.config[version]["bihome"] = bihome
        current_app.logger.info(f'bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(web_xml_file_path, 'w') as f:
            dom.writexml(f, encoding='utf-8')
        if reload:
            self.start_tomcat(version)
        return "bihome修改成功"

    def get_bi_home(self, version):
        if self.current_system == "Windows":
            split_str = '\\'
        else:
            split_str = '/'
        file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        dom = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        if param_value[-1] == entry_value[-1]:
            return param_value[-1]
        return "error bihome"

    def get_bi_port(self, version):
        file_path = f'{self.config[version]["path"]}{self.server_xml_path}'
        dom = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        connect = root.getElementsByTagName('Connector')
        port = connect[0].getAttribute('port')
        return port

    @staticmethod
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

    def is_port_used_fast(self, c_port):
        res = os.popen(f'netstat -ano |findstr {c_port}').read() if self.current_system == "Windows" else os.popen(
            f'lsof -i:{c_port}').read()
        if "LISTENING" in res or "LISTEN" in res:
            return True
        return False

    @staticmethod
    def current_time():
        return time.strftime("%H:%M:%S", time.localtime())

    def restart_tomcat(self, v, user=''):
        if self.config[v]['reload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境，请稍等'
            current_app.logger.info(f'[{user}] {res}')
            return res
        if self.config[v]['updateAndReload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境并更换jar包，请稍等'
            current_app.logger.info(f'[{user}] {res}')
            return res
        self.change_status(v, 'reload', True)
        self.shut_tomcat(v)
        self.start_tomcat(v, user)
        current_app.logger.info(f'[user]-{v} tomcat重启成功')
        self.change_status(v, 'reload')
        return f'{v} tomcat重启成功！'

    @staticmethod
    def get_pid_by_port_linux(port):
        res = os.popen(f'lsof -i:{port}').readlines()
        res.pop(0)
        pid = []
        for i in res:
            pid.append(i.split()[1])
        return ','.join(list(set(pid)))

    # 停止tomcat
    def shut_tomcat(self, v):
        check_res = self.check_status(v)
        if check_res != '0':
            return check_res
        self.change_status(v, 'shutdown', True)
        host_port = eval(self.config[v]["port"])
        if self.is_port_used(self.host_ip, host_port):
            if self.current_system == "Windows":
                current_app.logger.info(f'停止{v} tomcat进程')
                os.system(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
            else:
                work_dir = self.config[v]["path"] + self.tomcat_path
                os.chdir(work_dir)
                current_app.logger.info(f'进入目录{work_dir}')
                current_app.logger.info(f'执行命令：sh {work_dir}shutdown.sh')
                os.popen(f'sh {work_dir}shutdown.sh')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    current_app.logger.info(f'{v} tomcat服务停止中')
                else:
                    current_app.logger.info(f'{v} tomcat服务停止成功')
                    break
                time.sleep(30)
            self.change_status(v, 'shutdown')
            self.config[v]["status"] = '0'
            return f'{v} tomcat服务停止成功'
        else:
            self.change_status(v, 'shutdown')
            current_app.logger.info(f'{v} tomcat服务未启动')
            self.config[v]["status"] = '0'
            return f'{v} tomcat服务未启动'

    def start_tomcat(self, v, user=''):
        check_res = self.check_status(v)
        if check_res != '0':
            return check_res
        self.change_status(v, 'start', True)
        host_port = eval(self.config[v]["port"])
        work_dir = self.config[v]["path"] + self.tomcat_path
        os.chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.config[v]["status"] != '0':
                    current_app.logger.info(f'已启动{v} tomcat服务')
                    self.change_status(v, 'start')
                    self.config[v]["status"] = '1'
                    return f'已启动{v} tomcat服务'
                else:
                    current_app.logger.info('tomcat正在停止中')
                    time.sleep(10)
            else:
                if self.current_system == "Windows":
                    os.system('startup > caches.txt')
                else:
                    os.system('sh startup.sh > caches.txt')
                break
        current_app.logger.info(f'启动{v} tomcat服务成功')
        self.change_status(v, 'start')
        self.config[v]["status"] = '1'
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
        path0 = time.strftime("%Y%m%d", time.localtime())
        current_app.logger.info(f'当天的{version}jar包地址：{os.path.join(from_path_in, path0)}')
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
        current_app.logger.info(f'最新的是{path0}的包')
        return os.path.join(from_path_in, path0)

    def copy_jar(self, version, date=''):
        # self.toked[v]['update']=True
        self.change_status(version, 'update', True)
        """
        :param
        from_path_in:源路径
        to_path_in：目标路径
        version：版本号
        index：列表中下标
        """
        try:
            check_res = self.check_status(version)
            if check_res != '0':
                return check_res
            to_path_in = self.config[version]["path"] + self.YongHong_path
            branch = self.config[version]["branch"]
            backup_path = to_path_in + '/backup_product'
            if date != '':
                if os.path.exists(f'{self.ip}{branch}/{date}'):
                    path = f'{self.ip}{branch}/{date}'
                else:
                    # self.toked[v]['update']=False
                    self.change_status(version, 'update')
                    return f'{self.format_date_str(date)}的包不存在'
            else:
                path = self.get_recent_jar(version)
            dirs = os.listdir(path)
            if branch in ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']:
                path = path.replace(self.ip, self.ip_187)
            # 遍历目标地址中的项目jar
            for file_name in dirs:
                if branch == 'develop' and file_name not in ['api.jar', 'product.jar', 'thirds.jar']:
                    continue
                from_file = os.path.join(path, file_name)
                to_file = os.path.join(to_path_in, "product", file_name)
                if not os.path.exists(to_file):
                    self.rename_product_jar(file_name, os.path.join(to_path_in, "product"))
                try:
                    from_134_file = from_file.replace(self.ip, self.ip_134)
                    if os.path.exists(from_134_file):
                        if not filecmp.cmp(from_file, from_134_file):
                            from_file = from_134_file
                    if not os.path.exists(to_file):
                        copy2(from_file, to_file)
                        current_app.logger.info(f"{file_name}更新完毕,时间：{self.current_time()}")
                        continue
                    if not filecmp.cmp(from_file, to_file):
                        copy2(from_file, to_file)
                        current_app.logger.info(f"{file_name}更新完毕,时间：{self.current_time()}")
                except PermissionError:
                    self.change_status(version, 'update')
                    current_app.logger.info(f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
        except FileNotFoundError as err:
            self.change_status(version, 'update')
            current_app.logger.info(f'file error:{err}')
        current_app.logger.info(f'{version}-{self.format_date_str(date)} Jar包更新完成')
        self.change_status(version, 'update')
        return f'{version}-{self.format_date_str(date)} Jar包更新完成'

    def copy_and_reload(self, v, date='', user=''):
        # self.toked[v]['updateAndReload']=True
        self.change_status(v, 'updateAndReload', True)
        """
        :param v: 版本号 develop
        :return:
        """
        if self.config[v]['updateAndReload']:
            res = f'正在重启{v}环境并更换jar包，请稍等'
            current_app.logger.info(res)
            return res
        if self.config[v]['reload']:
            res = f'正在重启{v}环境，请稍等'
            current_app.logger.info(res)
            return res
        self.change_status(v, "updateAndReload", True)
        # 先关闭tomcat，然后换JAR，再启动tomcat
        self.shut_tomcat(v)
        self.copy_jar(v, date)
        self.start_tomcat(v, user)
        # self.toked[v]['updateAndReload']=False
        self.change_status(v, 'updateAndReload')
        return f'{v}已更换{self.format_date_str(date)} jar包并重启Tomcat成功'

    def new_copy(self, v, date=''):
        """
        :param date:
        :param v: 版本号 develop
        :return:
        """
        # self.toked[v]['update']=True
        self.change_status(v, 'update', True)
        self.copy_jar(v, date)
        current_app.logger.info(f'{v}-{self.format_date_str(date)} jar包检查完毕')
        # self.toked[v]['update']=False
        self.change_status(v, 'update')
        return f'{v}已更换{self.format_date_str(date)} jar包'

    def get_jar_list(self):
        jar_list = {}
        for key in self.config.keys():
            branch = self.config[key]["branch"]
            if branch in ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']:
                jar_list[key] = os.listdir(f'{self.ip_187}{branch}')
            else:
                jar_list[key] = os.listdir(f'{self.ip_134}{branch}')
            jar_list[key] = self.clear_list_not_num(jar_list[key])
            jar_list[key].sort()
            jar_list[key].reverse()
        return jar_list

    def check_status(self, v):
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
        current_app.logger.info(res)
        return res

    def change_status(self, v, key, flag=False):
        self.config[v][key] = flag
        self.update_product_status()

    def update_product_status(self):
        with open(self.status_path, 'w', encoding='utf-8') as status:
            json.dump(self.config, status)

    def get_jar_info(self, v):
        product_path = os.path.join(self.config[v]["path"], self.YongHong_path, 'product')
        info_list = []
        for i in os.listdir(product_path):
            change_time = time.strftime("日期:%Y%m%d 时间:%H:%M:%S",
                                        time.localtime(os.stat(os.path.join(product_path, i)).st_mtime))
            info_list.append(f"{i}:{change_time}")
            # print(f"{i}:{change_time}")
        return info_list
