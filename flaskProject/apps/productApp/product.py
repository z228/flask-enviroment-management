import os
from filecmp import cmp, cmpfiles
from json import dump, dumps, load
import pickle
from platform import system
from shutil import copy2, copytree, rmtree
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep, localtime, strftime
from xml.dom.minidom import parse
import re

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
    host_ip = '127.0.0.1'
    ip = '\\\\192.168.0.141/productJar/'
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
    root_path = ''
    YongHong_path = ''
    tomcat_path = ''
    bi_xml_path = ''
    server_xml_path = ''
    config = {}
    jar_list = {}
    release_jar_list = {}
    status = {}

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
        return dumps({"code": 200, "data": data}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def error(data=""):
        return dumps({"code": 500, "data": data}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def user_not_found(user):
        return dumps({"code": 405, "data": f"{user}用户不存在"}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def info(data=""):
        return dumps({"code": 205, "data": data}, ensure_ascii=False, separators=(',', ':'))

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
        self.update_product_status()
        # with open(f'{self.current_path}/apps/productApp/user.json', 'r', encoding='utf-8') as user:
        #     self.users = load(user)

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
        dom = parse(web_xml_file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        param_value[-1] = bihome
        entry_value[-1] = bihome
        self.config[version]["bihome"] = bihome
        product_logger.info(f'bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(web_xml_file_path, 'w') as f:
            dom.writexml(f, encoding='utf-8')
        if reload:
            self.start_tomcat(version)
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
            pass
        finally:
            return "error bihome"

    def get_bi_port(self, version):
        file_path = f'{self.config[version]["path"]}{self.server_xml_path}'
        dom = parse(file_path)
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
        if self.is_port_used(self.host_ip, host_port):
            if self.current_system == "Windows":
                product_logger.info(f'停止{v} tomcat进程')
                if v == 'trunk':
                    self.read_command(
                        f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
                else:
                    self.read_command(f"taskkill /f /pid {self.get_pid_by_port(host_port)}")
            else:
                work_dir = self.config[v]["path"] + self.tomcat_path
                os.chdir(work_dir)
                product_logger.info(f'进入目录{work_dir}')
                product_logger.info(f'执行命令：sh {work_dir}shutdown.sh')
                self.read_command(f'sh {work_dir}shutdown.sh')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    product_logger.info(f'{v} tomcat服务停止中')
                else:
                    product_logger.info(f'{v} tomcat服务停止成功')
                    break
                sleep(2)
            self.change_status(v, 'shutdown')
            self.config[v]["status"] = '0'
            return f'{v} tomcat服务停止成功'
        else:
            self.change_status(v, 'shutdown')
            product_logger.info(f'{v} tomcat服务未启动')
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
        # product_logger.info(self.read_command('pwd'))
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.config[v]["status"] != '0':
                    product_logger.info(f'已启动{v} tomcat服务')
                    self.change_status(v, 'start')
                    self.config[v]["status"] = '1'
                    return f'已启动{v} tomcat服务'
                else:
                    sleep(10)
                    product_logger.info('tomcat正在停止中')
            else:
                if self.current_system == "Windows":
                    os.system('startup > NUL')
                else:
                    self.read_command('sh startup.sh > caches.txt')
                break
        product_logger.info(f'启动{v} tomcat服务成功')
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
            return path_134
        return path_187 if os.path.exists(path_187) else path_134

    def new_copy(self, v, date='', copy_release=False, release=''):
        """
        复制jar包api
        :param v: 版本
        :param date: 日期
        :param copy_release: 是否复制release
        :param release: 发布版本
        :return:
        """
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
            # for file_name in dirs:
            #     if branch == 'develop' and file_name not in self.yonghong_product_jar:
            #         continue
            #     from_file = os.path.join(path, file_name)
            #     to_file = os.path.join(to_path_in, "product", file_name)
            #     if not os.path.exists(to_file):
            #         self.rename_product_jar(
            #             file_name, os.path.join(to_path_in, "product"))
            #     try:
            #         if not os.path.exists(to_file) or not cmp(from_file, to_file):
            #             copy2(from_file, to_file)
            #             product_logger.info(
            #                 f"{file_name}更新完毕,时间：{self.current_time()}")
            #             continue
            #     except PermissionError:
            #         self.change_status(version, 'update')
            #         product_logger.info(
            #             f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
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
        release_jar_path = f'{self.ip_187}common/{release_version}'
        local_jar_path = os.path.join(self.config[version]["path"] + self.YongHong_path, "product")
        res = self.cycle_copy(release_jar_path, local_jar_path, version)
        log_info = f'{version}-{release_version} Jar包更新完成' if res == 1 else res
        product_logger.info(log_info)
        self.change_status(version, 'update')
        return log_info

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
                    copytree(src, dst)  # 整个复制过来
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

    def copy_and_reload(self, v, date, user='', copy_release=False, release=''):
        """
        :param v: 版本
        :param date: jar包日期
        :param user: 用户
        :param copy_release: 是否复制release的jar包
        :param release: release版本
        :return:
        """
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
        res = self.copy_jar(v, date) if not copy_release else self.copy_release_jar(v, release)
        self.change_status(v, "updateAndReload", True)
        # 先关闭tomcat，然后换JAR，再启动tomcat
        self.start_tomcat(v, user)
        self.change_status(v, "updateAndReload")
        self.config[v]["startUser"] = user
        if "没有" not in res:
            return f'{v}已更换{self.format_date_str(date)} jar包并重启Tomcat成功'
        return res

    def get_jar_info(self, v):
        product_path = os.path.join(
            self.config[v]["path"] + self.YongHong_path, 'product')
        info_list = []
        for i in os.listdir(product_path):
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
            try:
                dir_134 = os.listdir(f'{self.ip_134}{branch}')
            except FileNotFoundError:
                product_logger.info("134服务器暂时无法连接")
                dir_134 = []
            finally:
                pass
            dir_134.extend(dir_187)
            dir_list = self.clear_list_dumplicate(dir_134)
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
        release_jar_path = f'{self.ip_187}common'
        for key in self.config.keys():
            branch = self.config[key]["branch"]
            jar_list[branch] = []
            if 'custom' in branch or branch == 'develop':
                continue
            if branch.replace('v', '') in exclude:
                continue
            branch_fmt_list = branch.replace('v', '').split('.')
            branch_fmt = f'{branch_fmt_list[0]}.{branch_fmt_list[1]}'
            for release in os.listdir(release_jar_path):
                if release in exclude or release == '9.4':
                    continue
                if branch_fmt in release:
                    jar_list[branch].append(release)
        return jar_list

    def get_bi_properties(self, v):
        bi_pro_path = os.path.join(self.config[v]["path"] + self.YongHong_path, self.config[v]["bihome"],
                                   'bi.properties')
        bi_pro = ''
        with open(bi_pro_path, 'r', encoding='utf-8') as biPro:
            bi_pro += biPro.read()
        return bi_pro

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
