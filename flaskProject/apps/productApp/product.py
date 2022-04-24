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
# from .status import toked
import platform
import _thread

from apps.productApp import status
if platform.system()=="Windows":
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
    config={}
    jar_list = {}
    status = {}
    toked = {}
    # current_system="linux"
    def __init__(self) -> None:
        self.readConfig()
        with open(self.status_path, 'r') as f:
            self.toked = json.load(f)
        if self.current_system == "Windows":
            self.jar_list = self.get_jar_list()

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
            if key not in self.toked.keys():
                self.toked[key]={}
                self.toked[key]['start']=False
                self.toked[key]['status']='0'
                self.toked[key]['shutdown']=False
                self.toked[key]['update']=False
                self.toked[key]['reload']=False
                self.toked[key]['updateAndReload']=False
            if 'dis' in key:
                self.config[key].append(self.config[key][1]+'/bi/?showOthers=true')
            else:
                self.config[key].append(self.config[key][1]+'/bi')
        self.change_status()

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
        current_app.logger.info(f'bihome修改为{bihome}')
        param[0].firstChild.data = split_str.join(param_value)
        entry[0].firstChild.data = split_str.join(entry_value)
        with open(file_path, 'w') as f:
            dom.writexml(f,encoding='utf-8')
        self.start_tomcat(version)
        return "bihome修改成功"

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

    def is_port_used_fast(self,c_port):
        if self.current_system == "Windows":
            res = os.popen(f'netstat -ano |findstr {c_port}').read()
            if "LISTENING" in res:
                return True
            return False
        else:
            res = os.popen(f'lsof -i:{c_port}').read()
            if "LISTEN" in res:
                return True
            return False

    def current_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def restart_tomcat(self,v,user=''):
        # self.toked[v]['reload']=True
        self.change_status(v,'reload',True)
        self.shut_tomcat(v)
        self.start_tomcat(v,user)
        current_app.logger.info(f'[user]-{v} tomcat重启成功')
        # self.toked[v]['reload']=False
        self.change_status(v,'reload',False)
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
        # self.toked[v]['shutdown']=True
        self.change_status(v,'shutdown',True)
        host_port = eval(self.config[v][1])
        if self.is_port_used(self.host_ip, host_port):
            if(self.current_system == "Windows"):
                current_app.logger.info(f'停止{v} tomcat进程')
                os.system(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
            else:
                work_dir = self.config[v][0] + self.tomcat_path
                os.chdir(work_dir)
                current_app.logger.info(f'进入目录{work_dir}')
                    # os.system(f'kill -9 {self.get_pid_by_port(str(host_port))}')
                current_app.logger.info(f'执行命令：sh {work_dir}shutdown.sh')
                os.popen(f'sh {work_dir}shutdown.sh')
            while 1:
                if self.is_port_used(self.host_ip, host_port):
                    current_app.logger.info(f'{v} tomcat服务停止中')
                else:
                    current_app.logger.info(f'{v} tomcat服务停止成功')
                    break
                time.sleep(30)
            # self.toked[v]['status']='0'
            self.change_status(v,'status','0')
            # self.toked[v]['shutdown']=False
            self.change_status(v,'shutdown',False)
            return f'{v} tomcat服务停止成功'
        else:
            # self.toked[v]['shutdown']=False
            self.change_status(v,'shutdown',False)
            current_app.logger.info(f'{v} tomcat服务未启动')
            return f'{v} tomcat服务未启动'

    def start_tomcat(self,v,user=''):
        # self.toked[v]['start']=True
        self.change_status(v,'start',True)
        # v = ip + v + '/'
        # index = from_path.index(v)
        host_port = eval(self.config[v][1])
        work_dir = self.config[v][0] + self.tomcat_path
        os.chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                if self.toked[v]['status']!='0':
                    current_app.logger.info(f'{self.toked[v]["status"]}已启动{v} tomcat服务')
                    return f'{self.toked[v]["status"]}已启动{v} tomcat服务'
                elif self.toked[v]['status']=='0':
                    current_app.logger.info('tomcat正在停止中')
                    time.sleep(10)
            else:
                if(self.current_system == "Windows"):
                    os.system('startup > caches.txt')
                else:
                    os.system('sh startup.sh > caches.txt')
                break
        current_app.logger.info(f'启动{v} tomcat服务成功')
        if user!='':
            # self.toked[v]['status']=user
            self.change_status(v,'status',user)
        # self.toked[v]['start']=False
        self.change_status(v,'start',False)
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
        # self.toked[v]['update']=True
        self.change_status(version,'update',True)
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
                    # self.toked[v]['update']=False
                    self.change_status(version,'update',True)
                    return f'{self.formatDateStr(date)}的包不存在'
            else:
                path = self.get_recent_jar(version)
            dirs = os.listdir(path)
            if version in ['v8.6','v9.0','v9.2.1','v9.4','develop']:
                path = path.replace(self.ip, self.ip_187)
            # 遍历目标地址中的项目jar
            for file_name in dirs:
                if version =='develop' and file_name not in ['api.jar','product.jar','thirds.jar']:
                    continue
                from_file = os.path.join(path, file_name)
                to_file = os.path.join(to_path_in, "product", file_name)
                if not os.path.exists(to_file):
                    self.renameProductJar(file_name,os.path.join(to_path_in, "product"))
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
                    self.change_status(version,'update',True)
                    current_app.logger.info(f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
        except FileNotFoundError as err:
            self.change_status(version,'update',True)
            current_app.logger.info(f'file error:{err}')
        current_app.logger.info(f'{version}-{self.formatDateStr(date)} Jar包更新完成')
        self.change_status(version,'update',True)
        return f'{version}-{self.formatDateStr(date)} Jar包更新完成'

    def copy_and_reload(self,v,date='',user=''):
        # self.toked[v]['updateAndReload']=True
        self.change_status(v,'updateAndReload',True)
        """
        :param v: 版本号 develop
        :return:
        """
        # 先关闭tomcat，然后换JAR，再启动tomcat
        self.shut_tomcat(v)
        self.copy_Jar(self.config[v][0] + self.YongHong_path, v,date)
        self.start_tomcat(v,user)
        # self.toked[v]['updateAndReload']=False
        self.change_status(v,'updateAndReload',False)
        return f'{v}已更换{self.formatDateStr(date)} jar包并重启Tomcat成功'

    def new_copy(self,v,date=''):
        """
        :param v: 版本号 develop
        :return:
        """
        # self.toked[v]['update']=True
        self.change_status(v,'update',True)
        self.copy_Jar(self.config[v][0] + self.YongHong_path, v,date)
        current_app.logger.info(f'{v}-{self.formatDateStr(date)} jar包检查完毕')
        # self.toked[v]['update']=False
        self.change_status(v,'update',False)
        return f'{v}已更换{self.formatDateStr(date)} jar包'

    def get_jar_list(self):
        jarList = {}
        for key in self.config.keys():
            key2 = "v9.4" if key == "v9.4.1"else key
            if key2 in ['v8.6','v9.0','v9.2.1','v9.4','develop']:
                jarList[key] = os.listdir(f'{self.ip_187}{key2}')
            else:
                jarList[key] = os.listdir(f'{self.ip_134}{key2}')
            jarList[key] = self.clear_list_not_num(jarList[key])
            jarList[key].sort()
            jarList[key].reverse()
        return jarList

    def check_product_status(self):
        v = {}
        end = len(self.config)
        start = 0
        mid = end//2
        _thread.start_new_thread(self.get_status_thread,(start,mid))
        _thread.start_new_thread(self.get_status_thread,(mid,end))
        # for key in self.config.keys():
        #     if self.is_port_used('localhost',eval(self.config[key][1])):
        #         if  key not in toked.keys():
        #             v[key] =''
        #         else:
        #             v[key] =toked[key]
        #     else:
        #         v[key] ='0'
        return self.status
    
    def get_status_thread(self,start,end,):
        ketList = list(self.config.keys())
        for i in range(start,end):
            if self.is_port_used('localhost',eval(self.config[ketList[i]][1])):
                if  ketList[i] not in toked.keys():
                    self.status[ketList[i]] =''
                else:
                    self.status[ketList[i]] =self.toked[ketList[i]]
            else:
                self.status[ketList[i]] ='0'
    
    def change_status(self,key1='',key2='',value=''):
        if key1 != '':
            self.toked[key1][key2] = value
        with open(self.status_path,'w') as status:
            json.dump(self.toked,status)

    def get_jar_info(self,v):
        product_paht = os.path.join(self.config[v][0],self.YongHong_path,'product')
        info_list = []
        for i in os.listdir(product_paht):
            change_time = time.strftime("日期:%Y%m%d 时间:%H:%M:%S",time.localtime(os.stat(os.path.join(product_paht,i)).st_mtime))
            info_list.append(f"{i}:{change_time}")
            # print(f"{i}:{change_time}")
        return info_list