# from _typeshed import Self
from filecmp import cmp, cmpfiles
from json import dump, loads, dumps
from logging import getLogger
from os import rename, listdir, system as sys, popen, chdir, stat, getcwd
from os.path import exists, join
from platform import system
from shutil import copy2
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep, localtime, strftime
from xml.dom.minidom import parse
from app import db, User

product_logger = getLogger("product")

if system() == "Windows":
    import win32api as api
    import win32console as con
    from . import properties
else:
    from . import properties_Linux as properties


class ProductAction:
    host_ip = '127.0.0.1'
    ip_141 = '/mnt/141/productJar/'  # 141挂载在187上的目录
    ip_134 = '/mnt/134/productJar/'  # 134挂载在187上的目录
    ip_187 = '/home/share/'  # 本地从134上实时copy过来的jar包
    ip = ip_134
    script_path = f"{getcwd()}/static/job"
    status_path = f"{getcwd()}/apps/productApp"
    day_31 = ['02', '04', '06', '08', '09', '11']
    current_system = system()  # 获取当前系统是windows还是linux
    codeType = {"default": ".py", "application/json": ".json", "sql": ".sql", "javascript": ".js", "css": ".css",
                "xml": ".xml", "html": ".html", "yaml": ".yml", "markdown": ".md", "python": ".py"}
    root_path = ''
    YongHong_path = ''  # Yonghong目录的路径
    tomcat_path = ''  # tomcat的路径
    bi_xml_path = ''  # tomcat下webapps/bi中bi.xml的路径
    server_xml_path = ''
    config = {}  # 所有环境的属性
    users = []

    def __init__(self) -> None:
        self.read_config()
        self.users = User.query.filter().all()

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
            return []
        new_array = [i for i in array if i.isdigit()]
        return new_array

    @staticmethod
    def clear_list_dumplicate(array=[]):
        new_array = list(set(array))
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
        res = popen(f'netstat -ano |findstr "{port}"').readlines()
        for i in res:
            if i.split()[-2] == 'LISTENING':
                product_logger.info(i)
                return i.split()[-1]

    @staticmethod
    def succ(data):
        return dumps({"code": 200, "data": data}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def error(data):
        return dumps({"code": 500, "data": data}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def user_not_found(user):
        return dumps({"code": 405, "data": f"{user}用户不存在"}, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def info(data):
        return dumps({"code": 205, "data": data}, ensure_ascii=False, separators=(',', ':'))

    # 获取脚本列表
    def get_all_script(self):
        job_list = {}
        index = 1
        for job in listdir(self.script_path):
            job_list[index] = {'name': job}
            index += 1
        product_logger.info(f'脚本列表：{job_list}')
        return job_list

    # 执行脚本
    def execute_script(self, task):
        if task.split('.')[1] != '.py':
            product_logger.info(f'{task}不是python脚本，无法执行')
            return f"非Python脚本无法执行"
        chdir(self.script_path)
        sys(f'python {task}')
        product_logger.info(f'{task}执行成功')
        return f'{task}执行成功'

    # 删除脚本
    def delete_script(self, task):
        chdir(self.script_path)
        sys(f'del {task}')
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
        status = {}
        if exists(f'{self.status_path}/status.json'):
            with open(f'{self.status_path}/status.json', 'r', encoding='utf-8') as f_status:
                str_status = f_status.read()
                status = loads(str_status) if len(str_status) != 0 else {}
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
        """
        get environment tomcat debug port
        :param version: 环境版本
        :return: 有端口返回端口值，没有就返回"未配置"
        """
        path = f'{self.config[version]["path"]}{self.tomcat_path}'
        catalina_path = f'{path}catalina.bat' if self.current_system == "Windows" else f'{path}catalina.sh'
        with open(catalina_path, 'r', encoding='utf-8') as catalina:
            catalina_lines = catalina.readlines()
            for i in catalina_lines:
                if 'export JPDA_ADDRESS=' in i and 'if [ -z "$JPDA_ADDRESS" ]; then' not in \
                        catalina_lines[catalina_lines.index(i) - 1]:
                    return i.split('=')[1].split(':')[1][0:-1]
        return "未配置"

    def change_bi_home(self, version, bihome, user=''):
        """
        change current bihome
        :param version: 环境版本
        :param bihome: 要切换的bihome的值
        :param user: 发送请求的用户
        :return:
        """
        split_str = '\\' if self.current_system == "Windows" else '/'
        reload = False
        if self.is_port_used('localhost', eval(self.config[version]["port"])):
            reload = True
        if reload:
            self.shut_tomcat(version)
        file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        dom = parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        param_value[-1] = bihome
        entry_value[-1] = bihome
        self.config[version]["bihome"] = bihome
        product_logger.info(f'[{user}] bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(file_path, 'w') as f:
            dom.writexml(f, encoding='utf-8')
        if reload:
            self.start_tomcat(version)
        return "bihome修改成功"

    def get_bi_home(self, version):
        """
        get current bihome
        :param version: 环境版本
        :return:
        """
        split_str = '\\' if self.current_system == "Windows" else '/'
        file_path = f'{self.config[version]["path"]}{self.bi_xml_path}'
        # dom = parse(file_path)
        # root = dom.documentElement
        root = self.get_web_xml(file_path)
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        if param_value[-1] == entry_value[-1]:
            return param_value[-1]
        return "error bihome"

    @staticmethod
    def get_web_xml(path):
        return parse(path).documentElement

    def get_bi_port(self, version):
        """
        get environment tomcat port
        :param version: 环境版本
        :return: 端口
        """
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
        :param c_ip: ip地址
        :param c_port: 端口号
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
    def current_time():
        return strftime("%H:%M:%S", localtime())

    def restart_tomcat(self, v, user=''):
        """
        reload the environment tomcat
        :param v: 环境版本
        :param user: 操作的用户
        :return: message
        """
        if self.config[v]['reload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        if self.config[v]['updateAndReload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境并更换jar包，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        self.change_status(v, "reload", True, user)
        self.shut_tomcat(v, user)
        self.start_tomcat(v, user)
        product_logger.info(f'[{user}]{v} tomcat重启成功')
        self.change_status(v, "reload")
        self.config[v]["startUser"] = user
        return f'{v} tomcat重启成功！'

    @staticmethod
    def get_pid_by_port(port):
        """
        get the pid by port
        :param port: 端口
        :return:
        """
        res = popen(f'lsof -i:{port}').readlines()
        res.pop(0)
        pid = [i.split()[1] for i in res]
        # for i in res:
        #     pid.append(i.split()[1])
        return ','.join(set(pid))

    # 停止tomcat
    def shut_tomcat(self, v, user=''):
        """
        shutdown environment tomcat
        :param v: 环境版本
        :param user: 操作的用户
        :return: message
        """
        check_res = self.check_status(v, user)
        if check_res != '0':
            return check_res
        self.change_status(v, "shutdown", True, user)
        host_port = eval(self.config[v]["port"])
        if self.is_port_used(self.host_ip, host_port):
            if self.current_system == "Windows":
                product_logger.info(f'[{user}]停止trunk tomcat进程')
                sys(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
            else:
                work_dir = self.config[v]["path"] + self.tomcat_path
                chdir(work_dir)
                if v == "trunk":
                    sys(f'sh  {self.config[v]["path"]}/tomcat/bin/shutdown.sh')
                else:
                    sys(f'kill -9 {self.get_pid_by_port(str(host_port))}')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    product_logger.info(f'[{user}]{v} tomcat服务停止中')
                else:
                    product_logger.info(f'[{user}]{v} tomcat服务停止成功')
                    break
                sleep(2)
            self.change_status(v, "shutdown")
            self.config[v]["startUser"] = ''
            return f'{v} tomcat服务停止成功'
        else:
            self.change_status(v, "shutdown")
            product_logger.info(f'[{user}]{v} tomcat服务未启动')
            return f'{v} tomcat服务未启动'

    def start_tomcat(self, v, user=''):
        """
        start environment tomcat
        :param v: 环境版本
        :param user: 操作的用户
        :return: message
        """
        check_res = self.check_status(v, user)
        if check_res != '0':
            return check_res
        self.change_status(v, "startup", True, user)
        host_port = eval(self.config[v]["port"])
        work_dir = self.config[v]["path"] + self.tomcat_path
        chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.config[v]["startUser"] != '':
                    self.change_status(v, "startup")
                    product_logger.info(f'[{user}] {self.config[v]["startUser"]}已启动{v} tomcat服务')
                    return f'{self.config[v]["startUser"]}已启动{v} tomcat服务'
                else:
                    product_logger.info('[{user}] tomcat正在停止中')
                    sleep(10)
            else:
                if self.current_system == "Windows":
                    sys('startup > caches.txt')
                else:
                    sys('sh catalina.sh jpda start > caches.txt')
                break
        product_logger.info(f'[{user}] 启动{v} tomcat服务成功')
        self.change_status(v, "startup")
        self.config[v]["startUser"] = user
        return f'启动{v} tomcat服务成功'

    @staticmethod
    def rename_product_jar(new_name, path):
        """
        rename jar
        :param new_name: jar的新名
        :param path: jar包路径
        :return:
        """
        jar_list = listdir(path)
        for i in jar_list:
            if i.split('.')[0] == 'product-swf':
                rename(f'{path}/{i}', f'{path}/product-swf.jar')
            elif new_name.split('.')[0] in i.split('.')[0]:
                rename(f'{path}/{i}', f'{path}/{new_name}')

    def get_recent_jar(self, version):
        git_branch = self.config[version]["branch"]
        from_path_in = f'{self.ip}{git_branch}'
        path0 = strftime("%Y%m%d", localtime())
        product_logger.info(f'当天的{version}jar包地址：{join(from_path_in, path0)}')
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not exists(join(from_path_in, path0)):
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
        return join(from_path_in, path0)

    def get_fast_path(self, version, date):
        """
        compare ip_187's jar with ip_134's jar,ip_187 preference
        :param version: 环境版本
        :param date: jar包日期
        :return:
        """
        git_branch = self.config[version]["branch"]
        path_187 = f'{self.ip_187}{git_branch}/{date}'
        path_134 = f'{self.ip}{git_branch}/{date}'
        if not exists(path_187) and not exists(path_134):
            product_logger.info(f'[system] {version}没有新的jar包')
            return ''
        common = ['api.jar', 'product.jar', 'thirds.jar']
        if exists(path_187) and exists(path_134):
            mismatch = cmpfiles(path_134, path_187, common)[1]
            if not mismatch:
                return path_187
            return path_134
        return path_187 if exists(path_187) else path_134

    def copy_jar(self, version, date, user=''):
        """
        copy jar from ip_187 or ip_134 to local
        :param
        from_path_in:源路径
        to_path_in：目标路径
        version：版本号
        """
        try:
            git_branch = self.config[version]["branch"]
            to_path_in = self.config[version]["path"] + self.YongHong_path
            check_res = self.check_status(version, user)
            if check_res != '0':
                return check_res
            self.change_status(version, "update", True, user)
            backup_path = to_path_in + '/backup_product'
            path = self.get_fast_path(version, date)
            if path == "" or date == "":
                self.change_status(version, "update")
                return f"{version}没有{'新' if date == '' else date}的jar包"
            # if date != '':
            #     if not exists(f'{path}'):
            #         self.change_status(version, "update")
            #         product_logger.info(f'{self.format_date_str(date)}的包不存在')
            #         return f'{self.format_date_str(date)}的包不存在'
            # else:
            #     path = self.get_recent_jar(version)
            # if exists(path_187):
            #     match, mismatch, errors = cmpfiles(path, path_187, common)
            #     path = path_187 if not mismatch else path
            dirs = listdir(path)
            # 遍历目标地址中的项目jar
            for file_name in dirs:
                from_file = join(path, file_name)
                to_file = join(to_path_in, "product", file_name)
                if not exists(to_file):
                    self.rename_product_jar(file_name, join(to_path_in, "product"))
                try:
                    # from_134_file = from_file.replace(self.ip, self.ip_134)
                    # if exists(from_134_file):
                    #     if not cmp(from_file, from_134_file):
                    #         from_file = from_134_file
                    if not exists(to_file) or not cmp(from_file, to_file):
                        copy2(from_file, to_file)
                        product_logger.info(f"[{user}] {file_name}更新完毕,时间：{self.current_time()}")
                        continue
                except PermissionError:
                    self.change_status(version, "update")
                    product_logger.info(f"[{user}] {path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
        except FileNotFoundError as err:
            self.change_status(version, "update")
            product_logger.info(f'[{user}] file error:{err}')
        date_format = self.format_date_str(date)
        product_logger.info(f'[{user}] {version}-{date_format} Jar包更新完成')
        self.change_status(version, "update")
        return f'{version}-{date_format} Jar包更新完成'

    def copy_and_reload(self, v, date, user=''):
        """
        update new jar and reload environment
        :param user: 操作的用户
        :param date: jar包日期
        :param v: 版本号 develop
        :return:
        """
        # 先关闭tomcat，然后换JAR，再启动tomcat
        if self.config[v]['updateAndReload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境并更换jar包，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        if self.config[v]['reload']:
            res = f'{self.config[v]["opUser"]} 正在重启{v}环境，请稍等'
            product_logger.info(f'[{user}] {res}')
            return res
        self.change_status(v, "updateAndReload", True, user)
        self.shut_tomcat(v, user)
        res = self.copy_jar(v, date, user)
        self.start_tomcat(v, user)
        self.change_status(v, "updateAndReload")
        self.config[v]["startUser"] = user
        if "没有" not in res:
            return f'{v}已更换{self.format_date_str(date)} jar包并重启Tomcat成功'
        return res

    def get_jar_info(self, v):
        """
        get the jar dateTime
        :param v: 环境版本
        :return:
        """
        product_path = join(self.config[v]["path"] + self.YongHong_path, 'product')
        info_list = []
        for i in listdir(product_path):
            change_time = strftime("日期:%Y%m%d 时间:%H:%M:%S", localtime(stat(join(product_path, i)).st_mtime))
            info_list.append(f"{i}:{change_time}")
        return info_list

    def get_jar_list(self):
        """
        get jar list from ip_187 and ip_134
        :return:
        """
        jar_list = {}
        for key in self.config.keys():
            branch = self.config[key]["branch"]
            dir_187 = listdir(f'{self.ip_187}{branch}') if exists(f'{self.ip_187}{branch}') else []
            dir_134 = listdir(f'{self.ip_134}{branch}')
            dir_134.extend(dir_187)
            dir_list = self.clear_list_dumplicate(dir_134)
            jar_list[key] = dir_list
            jar_list[key] = self.clear_list_not_num(jar_list[key])
            jar_list[key].sort()
            jar_list[key].reverse()
        return jar_list

    def get_bi_properties(self, v):
        """
        get key-value of environment bi.properties
        :param v: 环境版本
        :return:
        """
        bi_pro_path = join(self.config[v]["path"] + self.YongHong_path, self.config[v]["bihome"],
                           'bi.properties')
        bi_pro = ''
        with open(bi_pro_path, 'r', encoding='utf-8') as biPro:
            bi_pro += biPro.read()
        return bi_pro

    def update_product_status(self):
        """
        update all environments status and dump to status.json
        :return:
        """
        with open(f'{self.status_path}/status.json', 'w', encoding='utf-8') as status:
            dump(self.config, status, indent=4)

    def check_status(self, v, user=''):
        """
        check environment status
        :param v:
        :param user:
        :return:
        """
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
        if res != '0':
            product_logger.info(f'[{user}] {res}')
        return res

    def change_status(self, v, key, flag=False, op_user=''):
        """
        change environment status,default false
        :param v:
        :param key:
        :param flag:
        :param op_user:
        :return:
        """
        self.config[v][key] = flag
        self.config[v]["opUser"] = op_user
        self.update_product_status()

    def change_junit_exp(self, case_list):
        path_199 = r''
        module = case_list['module']
        version = case_list['version']
        cases = case_list['cases']
        module_path = fr"assetExecute/testcases/{module}"
        with open(f'{self.status_path}/cases.json', 'w', encoding='utf-8') as cases:
            dump(case_list, cases, indent=4, ensure_ascii=False)

    def user_validation(self, userinfo):
        username = userinfo['username'].strip().lower()
        passwd = userinfo['password']
        user = self.get_user_by_username(username)
        if user:
            return self.succ("登录成功") if passwd == user.password else self.info("密码错误")
        return self.info("用户不存在")

    def get_user_by_username(self, username):
        user_info = User.query.filter(User.username == username.strip().lower()).first()
        if user_info:
            return user_info
        for user in self.users:
            if username.strip().lower() in user.alias:
                return user
        return ""

    def update_userlist(self):
        self.users = User.query.filter().all()

    def update_userinfo(self, userinfo):
        user_id = userinfo["userId"]
        username = userinfo["username"]
        password = userinfo["password"]
        alias = userinfo["alias"]
        email = userinfo["email"]
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            if self.get_user_by_username(username):
                return self.info("用户名已存在")
            change = (user.username != username) | (user.password != password) | (user.alias != alias) | (
                    user.email != email)
            if change:
                user.username = username
                user.password = password
                user.alias = alias
                user.email = email
                # db.session.add(user)
                db.session.commit()
                self.update_userlist()
                return self.succ("用户信息修改成功")
            return self.info("用户信息无变化")
        return self.info("用户不存在")

    def create_new_user(self, userinfo):
        username = userinfo["username"]
        password = userinfo["password"]
        alias = userinfo["alias"]
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
        user = User.query.filter(User.username == username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            self.update_userlist()
            return self.succ("用户删除成功")
        return self.info("用户不存在")
