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
import platform

if platform.system() == "Windows":
    import win32api as api
    import win32console as con
    from . import properties
else:
    from . import properties_Linux as properties


class ProductAction:
    host_ip = '127.0.0.1'
    ip = '/mnt/141/productJar/'
    ip_134 = '/mnt/134/productJar/'
    ip_local = '/home/share/'
    ip = ip_134
    from_path = []
    script_path = f"{os.getcwd()}/static/job"
    status_path = f"{os.getcwd()}/apps/productApp"
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

    # current_system="linux"
    def __init__(self) -> None:
        self.read_config()

    # 向某个进程发送ctrl+c指令
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
        :param date_str: 日期字符串
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
    def error(data):
        return json.dumps({"code": 500, "data": data})

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
        status = {}
        if os.path.exists(f'{self.status_path}/status.json'):
            with open(f'{self.status_path}/status.json', 'r', encoding='utf-8') as f_status:
                str_status = f_status.read()
                status = json.loads(str_status) if len(str_status) != 0 else {}
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
                self.config[key]["url"] = self.config[key]["port"] + '/bi/?showOthers=true'
            else:
                self.config[key]["url"] = self.config[key]["port"] + '/bi'
            self.config[key]["debug"] = self.get_debug_port(key)
            self.config[key]["startup"] = False
            self.config[key]["shutdown"] = False
            self.config[key]["update"] = False
            self.config[key]["reload"] = False
            self.config[key]["updateAndReload"] = False
            self.config[key]["changeBihome"] = False
            self.config[key]["opUser"] = ''
            self.config[key]["startUser"] = status[key]["startUser"] if key in status.keys() else ''
        self.update_product_status()

    def get_debug_port(self, version):
        catalina_path = f'{self.config[version]["path"]}{self.tomcat_path}catalina.bat' if self.current_system == "Windows" else f'{self.config[version]["path"]}{self.tomcat_path}catalina.sh'
        with open(catalina_path, 'r', encoding='utf-8') as catalina:
            catalina_lines = catalina.readlines()
            for i in catalina_lines:
                if 'export JPDA_ADDRESS=' in i and 'if [ -z "$JPDA_ADDRESS" ]; then' not in \
                        catalina_lines[catalina_lines.index(i) - 1]:
                    return i.split('=')[1].split(':')[1][0:-1]
        return "未配置"

    def change_bi_home(self, version, bihome, user=''):
        split_str = '\\' if self.current_system == "Windows" else '/'
        reload = False
        if self.is_port_used('localhost', eval(self.config[version]["port"])):
            reload = True
        if reload:
            self.shut_tomcat(version)
        file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        dom = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        param_value[-1] = bihome
        entry_value[-1] = bihome
        self.config[version]["bihome"] = bihome
        current_app.logger.info(f'[{user}] bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(file_path, 'w') as f:
            dom.writexml(f, encoding='utf-8')
        if reload:
            self.start_tomcat(version)
        return "bihome修改成功"

    def get_bi_home(self, version):
        split_str = '\\' if self.current_system == "Windows" else '/'
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
        self.change_status(v, "reload", True, user)
        self.shut_tomcat(v, user)
        self.start_tomcat(v, user)
        current_app.logger.info(f'[{user}]{v} tomcat重启成功')
        self.change_status(v, "reload")
        self.config[v]["startUser"] = user
        return f'{v} tomcat重启成功！'

    @staticmethod
    def get_pid_by_port(port):
        res = os.popen(f'lsof -i:{port}').readlines()
        res.pop(0)
        pid = []
        for i in res:
            pid.append(i.split()[1])
        return ','.join(list(set(pid)))

    # 停止tomcat
    def shut_tomcat(self, v, user=''):
        check_res = self.check_status(v, user)
        if check_res != '0':
            return check_res
        self.change_status(v, "shutdown", True, user)
        host_port = eval(self.config[v]["port"])
        if self.is_port_used(self.host_ip, host_port):
            if self.current_system == "Windows":
                current_app.logger.info(f'[{user}]停止trunk tomcat进程')
                os.system(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
            else:
                work_dir = self.config[v]["path"] + self.tomcat_path
                os.chdir(work_dir)
                if v == "develop":
                    os.system(f'sh  {self.config[v]["path"]}/tomcat/bin/shutdown.sh')
                else:
                    os.system(f'kill -9 {self.get_pid_by_port(str(host_port))}')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    current_app.logger.info(f'[{user}]{v} tomcat服务停止中')
                else:
                    current_app.logger.info(f'[{user}]{v} tomcat服务停止成功')
                    break
                time.sleep(2)
            self.change_status(v, "shutdown")
            self.config[v]["startUser"] = ''
            return f'{v} tomcat服务停止成功'
        else:
            self.change_status(v, "shutdown")
            current_app.logger.info(f'[{user}]{v} tomcat服务未启动')
            return f'{v} tomcat服务未启动'

    def start_tomcat(self, v, user=''):
        check_res = self.check_status(v, user)
        if check_res != '0':
            return check_res
        self.change_status(v, "startup", True, user)
        host_port = eval(self.config[v]["port"])
        work_dir = self.config[v]["path"] + self.tomcat_path
        os.chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.config[v]["startUser"] != '':
                    self.change_status(v, "startup")
                    current_app.logger.info(f'[{user}] {self.config[v]["startUser"]}已启动{v} tomcat服务')
                    return f'{self.config[v]["startUser"]}已启动{v} tomcat服务'
                else:
                    current_app.logger.info('[{user}] tomcat正在停止中')
                    time.sleep(10)
            else:
                if self.current_system == "Windows":
                    os.system('startup > caches.txt')
                else:
                    os.system('sh catalina.sh jpda start > caches.txt')
                break
        current_app.logger.info(f'[{user}] 启动{v} tomcat服务成功')
        self.change_status(v, "startup")
        self.config[v]["startUser"] = user
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
        git_branch = self.config[version]["branch"]
        from_path_in = f'{self.ip}{git_branch}'
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

    def copy_jar(self, version, date='', user=''):
        """
        :param
        from_path_in:源路径
        to_path_in：目标路径
        version：版本号
        index：列表中下标
        """
        try:
            git_branch = self.config[version]["branch"]
            to_path_in = self.config[version]["path"] + self.YongHong_path
            check_res = self.check_status(version, user)
            if check_res != '0':
                return check_res
            self.change_status(version, "update", True, user)
            backup_path = to_path_in + '/backup_product'
            if date != '':
                if os.path.exists(f'{self.ip}{git_branch}/{date}'):
                    path = f'{self.ip}{git_branch}/{date}'
                else:
                    self.change_status(version, "update")
                    return f'{self.format_date_str(date)}的包不存在'
            else:
                path = self.get_recent_jar(version)
            dirs = os.listdir(path)
            if git_branch in ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']:
                path = path.replace(self.ip, self.ip_local)
            # 遍历目标地址中的项目jar
            for file_name in dirs:
                from_file = os.path.join(path, file_name)
                to_file = os.path.join(to_path_in, "product", file_name)
                if not os.path.exists(to_file):
                    self.rename_product_jar(file_name, os.path.join(to_path_in, "product"))
                # backup_file = os.path.join(backup_path, file_name)
                try:
                    from_134_file = from_file.replace(self.ip, self.ip_134)
                    # if os.path.exists(from_134_file):
                    #     if not filecmp.cmp(from_file, from_134_file):
                    #         from_file = from_134_file
                    if not os.path.exists(to_file):
                        copy2(from_file, to_file)
                        current_app.logger.info(f"[{user}] {file_name}更新完毕,时间：{self.current_time()}")
                        continue
                    if not filecmp.cmp(from_file, to_file):
                        copy2(from_file, to_file)
                        current_app.logger.info(f"[{user}] {file_name}更新完毕,时间：{self.current_time()}")
                except PermissionError:
                    self.change_status(version, "update")
                    current_app.logger.info(f"[{user}] {path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
        except FileNotFoundError as err:
            self.change_status(version, "update")
            current_app.logger.info(f'[{user}] file error:{err}')
        current_app.logger.info(f'[{user}] {version}-{self.format_date_str(date)} Jar包更新完成')
        self.change_status(version, "update")
        return f'{version}-{self.format_date_str(date)} Jar包更新完成'

    def copy_and_reload(self, v, date='', user=''):
        """
        :param user:
        :param date:
        :param v: 版本号 develop
        :return:
        """
        # 先关闭tomcat，然后换JAR，再启动tomcat
        if self.config[v]['updateAndReload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境并更换jar包，请稍等'
            current_app.logger.info(f'[{user}] {res}')
            return res
        if self.config[v]['reload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境，请稍等'
            current_app.logger.info(f'[{user}] {res}')
            return res
        self.change_status(v, "updateAndReload", True, user)
        self.shut_tomcat(v, user)
        self.copy_jar(v, date, user)
        self.start_tomcat(v, user)
        self.change_status(v, "updateAndReload")
        self.config[v]["startUser"] = user
        return f'{v}已更换{self.format_date_str(date)} jar包并重启Tomcat成功'

    def get_jar_info(self, v):
        product_path = os.path.join(self.config[v]["path"] + self.YongHong_path, 'product')
        info_list = []
        for i in os.listdir(product_path):
            change_time = time.strftime("日期:%Y%m%d 时间:%H:%M:%S",
                                        time.localtime(os.stat(os.path.join(product_path, i)).st_mtime))
            info_list.append(f"{i}:{change_time}")
        return info_list

    def get_bi_properties(self, v):
        bi_pro_path = os.path.join(self.config[v]["path"] + self.YongHong_path, self.config[v]["bihome"],
                                   'bi.properties')
        bi_pro = ''
        with open(bi_pro_path, 'r', encoding='utf-8') as biPro:
            bi_pro += biPro.read()
        return bi_pro

    def update_product_status(self):
        with open(f'{self.status_path}/status.json', 'w', encoding='utf-8') as status:
            json.dump(self.config, status)

    def check_status(self, v, user=''):
        status = self.config[v]
        if status['startup']:
            res = f'{status["opUser"]} 已启动{v}环境，请刷新'
        elif status['shutdown']:
            res = f'{status["opUser"]} 正在关闭{v}环境，请稍等'
        elif status['update']:
            res = f'{status["opUser"]} 正在更新{v}环境jar包，请稍等'
        elif status['changeBihome']:
            res = f'{status["opUser"]} 正在更换{v}bihome路径，请稍等'
        else:
            res = '0'
        if res!='0':
            current_app.logger.info(f'[{user}] {res}')
        return res

    def change_status(self, v, key, flag=False, op_user=''):
        self.config[v][key] = flag
        self.config[v]["opUser"] = op_user
        self.update_product_status()
