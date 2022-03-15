# from _typeshed import Self
import imp
import os
import time
from shutil import copy2, rmtree
import filecmp
import socket
import json
from flask import current_app
import  xml.dom.minidom
from .status import toked
import platform
if platform.system()=="Windows":
    import win32api as api
    import win32console as con
    from . import properties
else:
    from . import properties_Linux as properties

class ProductAction:
    host_ip = '127.0.0.1'
    ip = '/mnt/141/productJar/'
    ip_134 = '/mnt/134/productJar/'
    ip = ip_134
    from_path = []
    script_path = f"{os.getcwd()}/static/job"
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
    config={}
    # current_system="linux"
    def __init__(self) -> None:
        self.readConfig()

    # 向某个进程发送crtl+c指令
    def send_ctrl_c(self,pid):
        con.FreeConsole()
        if con.AttachConsole(int(pid)) == None:
            api.SetConsoleCtrlHandler(None, 1)
            api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
            api.Sleep(15)
            con.FreeConsole()
            api.SetConsoleCtrlHandler(None, 0)

    def clear_list_not_num(self,array=[]):
        """
        :param array: 日期列表
        :return:清空非纯数字的子项
        """
        newArray = []
        for i in array:
            if i.isdigit():
                newArray.append(i)
        return newArray
    
    def formatDateStr(self,str=''):
        """
        :param str:日期字符串
        :return:返回格式化后的字符串
        """
        if str=='':
            return str
        return f"{str[0:4]}-{str[4:6]}-{str[6:8]}"

    # 通过host+port获取进程pid
    def get_pid_from_port(self,port):
        res = os.popen(f'netstat -ano |findstr "{port}"').readlines()
        for i in res:
            if i.split()[-2] == 'LISTENING':
                current_app.logger.info(i)
                return i.split()[-1]

    def succ(self,data):
        return json.dumps({"code": 200, "data": data})

    def error(self,data):
        return json.dumps({"code": 500, "data": data})
    
    def info(self,data):
        return json.dumps({"code": 205, "data": data})

    # 获取脚本列表
    def getAllScript(self):
        job_list = {}
        index = 1
        for job in os.listdir(self.script_path):
            job_list[index] = {'name': job}
            index += 1
        current_app.logger.info(f'脚本列表：{job_list}')
        return job_list

    # 执行脚本
    def executeScript(self,task):
        if task.split('.')[1]!='.py':
            current_app.logger.info(f'{task}不是python脚本，无法执行')
            return f"非Python脚本无法执行"
        os.chdir(self.script_path)
        os.system(f'python {task}')
        current_app.logger.info(f'{task}执行成功')
        return f'{task}执行成功'

    # 删除脚本
    def deleteScript(self,task):
        os.chdir(self.script_path)
        os.system(f'del {task}')
        current_app.logger.warning(f'{task}删除成功')
        return f'{task}删除成功'

    # 保存脚本
    def saveScript(self,content, name, type):
        end = self.codeType[type]
        script = name + end
        with open(f'{self.script_path}/{script}', 'w', encoding='utf-8') as newScript:
            newScript.write(content)
        current_app.logger.info(f'{script}保存成功')
        return f'{script}保存成功'

    # 读取配置文件
    def readConfig(self):
        self.config = properties.env_list['version']
        self.root_path = properties.env_list["mid_path"]
        self.YongHong_path = f'{self.root_path}/Yonghong'
        self.tomcat_path = f'{self.root_path}/tomcat/bin/'
        self.bi_xml_path = f'{self.root_path}/tomcat/webapps/bi/WEB-INF/web.xml'
        self.server_xml_path = f'{self.root_path}/tomcat/conf/server.xml'
        for key in self.config.keys():
            self.config[key][1] = self.get_bi_port(key)
            self.config[key].append(self.get_bi_home(key))
            if 'dis' in key:
                self.config[key].append('/bi/?showOthers=true')
            else:
                self.config[key].append('/bi')

    def get_debug_port(self,version):
        if self.current_system == "Windows":
            catalina_path = f'{self.config[version][0]}{self.tomcat_path}catalina.bat'
        else:
            catalina_path = f'{self.config[version][0]}{self.tomcat_path}catalina.sh'
        with open(catalina_path,'r',encoding='utf-8') as catalina:
            for i in catalina.readlines():
                if 'JPDA_ADDRESS' in i:
                    return i.split('=')[1].split(':')[1][0:-1]

    def change_bi_home(self,version,bihome):
        if self.current_system == "Windows":
            split_str = '\\'
        else:
            split_str = '/'
        reload = False
        if self.is_port_used('localhost',eval(self.config[version][1])):
            reload = True
        if reload == True:
            self.shut_tomcat(version)
        file_path = f'{self.config[version][0]}{self.bi_xml_path}'
        dom  = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        param_value[-1] = bihome
        entry_value[-1] = bihome
        self.config[version][3] = bihome
        current_app.logger.info(f'bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(file_path, 'w') as f:
            dom.writexml(f,encoding='utf-8')
        if reload == True:
            self.start_tomcat(version)
        return "bihome修改成功"

    def get_bi_home(self,version):
        if self.current_system == "Windows":
            split_str = '\\'
        else:
            split_str = '/'
        file_path = f'{self.config[version][0]}{self.bi_xml_path}'
        dom  = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split(split_str)
        entry_value = entry[0].firstChild.data.split(split_str)
        if param_value[-1] == entry_value[-1]:
            return param_value[-1]
        return "error bihome"

    def get_bi_port(self,version):
        file_path = f'{self.config[version][0]}{self.server_xml_path}'
        dom  = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        connect = root.getElementsByTagName('Connector')
        port = connect[0].getAttribute('port')
        return port

    def is_port_used(self,c_ip, c_port):
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

    def current_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def restart_tomcat(self,v,user=''):
        self.shut_tomcat(v)
        self.start_tomcat(v,user)
        current_app.logger.info(f'{v} tomcat重启成功')
        return f'{v} tomcat重启成功！'

    def get_pid_by_port(self,port):
        res = os.popen(f'lsof -i:{port}').readlines()
        res.pop(0)
        pid =[]
        for i in res:
            pid.append(i.split()[1])
        return ','.join(list(set(pid)))
        

    # 停止tomcat
    def shut_tomcat(self,v):
        host_port = eval(self.config[v][1])
        if self.is_port_used(self.host_ip, host_port):
            if(self.current_system == "Windows"):
                # if v == 'develop':
                    # print('停止trunk tomcat进程')
                # print(os.getcwd())
                current_app.logger.info('停止trunk tomcat进程')
                os.system(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
                # else:
                #     work_dir = self.config[v][0] + self.tomcat_path
                #     os.chdir(work_dir)
                #     os.system(f'shutdown > caches.txt')
            else:
                work_dir = self.config[v][0] + self.tomcat_path
                os.chdir(work_dir)
                os.system(f'kill -9 {self.get_pid_by_port(str(host_port))}')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    current_app.logger.info(f'{v} tomcat服务停止中')
                else:
                    current_app.logger.info(f'{v} tomcat服务停止成功')
                    break
                time.sleep(2)
            toked[v]=''
            return f'{v} tomcat服务停止成功'
        else:
            current_app.logger.info(f'{v} tomcat服务未启动')
            return f'{v} tomcat服务未启动'

    def start_tomcat(self,v,user=''):
        # v = ip + v + '/'
        # index = from_path.index(v)
        host_port = eval(self.config[v][1])
        work_dir = self.config[v][0] + self.tomcat_path
        os.chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if toked[v]!='':
                    current_app.logger.info(f'{toked[v]}已启动{v} tomcat服务')
                    return f'{toked[v]}已启动{v} tomcat服务'
                elif toked[v]=='':
                    current_app.logger.info('tomcat正在停止中')
                    time.sleep(10)
            else:
                if(self.current_system == "Windows"):
                    os.system('startup > caches.txt')
                else:
                    os.system('sh catalina.sh jpda start > caches.txt')
                break
        current_app.logger.info(f'启动{v} tomcat服务成功')
        if user!='':
            toked[v]=user
        return f'启动{v} tomcat服务成功'

    def renameProductJar(self,newName,path):
        jar_list=os.listdir(path)
        for i in jar_list:
            if i.split('.')[0]=='product-swf':
                os.rename(f'{path}/{i}',f'{path}/product-swf.jar')
            elif newName.split('.')[0] in i.split('.')[0]:
                os.rename(f'{path}/{i}',f'{path}/{newName}')
    
    def get_recent_jar(self,version):
        if version =='v9.4.1':
            version='v9.4'
        if version == 'develop':
            from_path_in = f'{self.ip}{version}'
        else:
            from_path_in = f'{self.ip}{version}'
        path0 = time.strftime("%Y%m%d", time.localtime())
        current_app.logger.info(f'当天的{version}jar包地址：{os.path.join(from_path_in, path0)}')
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

    def copy_Jar(self,to_path_in, version, date=''):
        """
        :param
        from_path_in:源路径
        to_path_in：目标路径
        version：版本号
        index：列表中下标
        """
        try:
            if version =='v9.4.1':
                version='v9.4'
            backup_path = to_path_in + '/backup_product'
            if date !='':
                if os.path.exists(f'{self.ip}{version}/{date}'):
                    path = f'{self.ip}{version}/{date}'
                else:
                    return f'{self.formatDateStr(date)}的包不存在'
            else:
                path = self.get_recent_jar(version)
            dirs = os.listdir(path)
            # 遍历目标地址中的项目jar
            for file_name in dirs:
                from_file = os.path.join(path, file_name)
                to_file = os.path.join(to_path_in, "product", file_name)
                if not os.path.exists(to_file):
                    self.renameProductJar(file_name,os.path.join(to_path_in, "product"))
                # backup_file = os.path.join(backup_path, file_name)
                try:
                    from_134_file = from_file.replace(self.ip, self.ip_134)
                    # if os.path.exists(from_134_file):
                    #     if not filecmp.cmp(from_file, from_134_file):
                    #         from_file = from_134_file
                    if not filecmp.cmp(from_file, to_file):
                        # copy2(to_file, backup_file)
                        copy2(from_file, to_file)
                        # copy2(from_file, ubuntu_file)
                        current_app.logger.info(f"{file_name}更新完毕,时间：{self.current_time()}")
                except PermissionError:
                    current_app.logger.info(f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
        except FileNotFoundError as err:
            current_app.logger.info(f'file error:{err}')
        current_app.logger.info(f'{version}-{self.formatDateStr(date)} Jar包更新完成')
        return f'{version}-{self.formatDateStr(date)} Jar包更新完成'

    def copy_and_reload(self,v,date='',user=''):
        """
        :param v: 版本号 develop
        :return:
        """
        # 先关闭tomcat，然后换JAR，再启动tomcat
        self.shut_tomcat(v)
        self.copy_Jar(self.config[v][0] + self.YongHong_path, v,date)
        self.start_tomcat(v,user)
        return f'{v}已更换{self.formatDateStr(date)} jar包并重启Tomcat成功'

    def new_copy(self,v,date=''):
        """
        :param v: 版本号 develop
        :return:
        """
        self.copy_Jar(self.config[v][0] + self.YongHong_path, v,date)
        current_app.logger.info(f'{v}-{self.formatDateStr(date)} jar包检查完毕')
        return f'{v}已更换{self.formatDateStr(date)} jar包'
