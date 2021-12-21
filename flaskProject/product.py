from ntpath import join
import os
import signal
import time
from shutil import copy2, rmtree
import filecmp
import socket
from task import clean_jar
import json
from flask import current_app
import  xml.dom.minidom
import platform
import properties
if platform.system()=="Windows":
    import win32api as api
    import win32console as con

class ProductAction:
    host_ip = '127.0.0.1'
    ip = '\\\\192.168.0.141/productJar/'
    ip_134 = '\\\\192.168.1.134/git-package/'
    from_path = []
    script_path = f"f{os.getcwd()}/static/job"
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

    # 向某个进程发送crtl+c指令
    def send_ctrl_c(self,pid):
        con.FreeConsole()
        if con.AttachConsole(int(pid)) == None:
            api.SetConsoleCtrlHandler(None, 1)
            api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
            api.Sleep(15)
            con.FreeConsole()
            api.SetConsoleCtrlHandler(None, 0)

    # 通过host+port获取进程pid
    def get_pid_from_port(self,port):
        res = os.popen(f'netstat -ano |findstr "{port}"').readlines()
        for i in res:
            if i.split()[-2] == 'LISTENING':
                print(i)
                return i.split()[-1]


    def succ(self,data):
        return json.dumps({"code": 200, "data": data})


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
        # with open('properties.json', 'r', encoding='utf-8') as properties:
        #     property_dict = json.load(properties)
        #     self.config = property_dict['version']
            # for i in property_dict["version"].keys():
            #     pass
                # from_path.append(f'{ip}{i}/')
                # to_path.append(property_dict["version"][i][0])
                # port.append(property_dict["version"][i][1])
                # ubuntu_path.append(property_dict["version"][i][2])
            # self.root_path = property_dict["mid_path"]
        self.config = properties.env_list['version']
        self.root_path = properties.env_list["mid_path"]
        self.YongHong_path = f'{self.root_path}/Yonghong'
        self.tomcat_path = f'{self.root_path}/tomcat/bin/'
        self.bi_xml_path = f'{self.root_path}/tomcat/webapps/bi/WEB-INF/web.xml'


    def change_bi_home(self,version,bihome):
        self.shut_tomcat(version)
        file_path = f'{self.config[version][0]}{self.bi_xml_path}'
        dom  = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        param = root.getElementsByTagName('param-value')
        entry = root.getElementsByTagName('env-entry-value')
        param_value = param[0].firstChild.data.split('\\')
        entry_value = entry[0].firstChild.data.split('\\')
        param_value[-1] = bihome
        entry_value[-1] = bihome
        current_app.logger.info(f'bihome修改为{bihome}')
        param[0].firstChild.data = '\\'.join(param_value)
        entry[0].firstChild.data = '\\'.join(entry_value)
        print(f'bihome修改为：{param[0].firstChild.data}')
    # D:\old_version\9.4.1\Yonghong_Z-Suite\Yonghong\bihome
        with open(file_path, 'w') as f:
            dom.writexml(f,encoding='utf-8')
        self.start_tomcat(version)
        return "bihome修改成功"


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


    def restart_tomcat(self,v):
        log = f'{self.current_time}<p>'
        log += self.shut_tomcat(v)
        log += self.start_tomcat(v)
        current_app.logger.info(f'{v}tomcat重启成功')
        return f'{v}tomcat重启成功！'


    # 停止tomcat
    def shut_tomcat(self,v):
        host_port = eval(self.config[v][1])
        if self.is_port_used(self.host_ip, host_port):
            if(self.current_system == "Windows"):
                if v == 'develop':
                    print('停止trunk tomcat进程')
                    os.system(f'python {self.script_path}/stopTrunk.py {host_port} > stopTomcat.txt')
                else:
                    work_dir = self.config[v][0] + self.tomcat_path
                    os.chdir(work_dir)
                    os.system('shutdown')
            else:
                work_dir = self.config[v][0] + self.tomcat_path
                os.chdir(work_dir)
                os.system('sh shutdown.sh')
            current_app.logger.info(f'{v}tomcat服务停止成功')
            return f'{v}tomcat服务停止成功'
        else:
            current_app.logger.info(f'{v}tomcat服务未启动')
            return f'{v}tomcat服务未启动'


    def start_tomcat(self,v):
        # v = ip + v + '/'
        # index = from_path.index(v)
        host_port = eval(self.config[v][1])
        work_dir = self.config[v][0] + self.tomcat_path
        os.chdir(work_dir)
        for scape in range(100):
            if self.is_port_used(self.host_ip, host_port):
                print('tomcat正在停止中')
                time.sleep(10)
            else:
                if(self.current_system == "Windows"):
                    os.system('startup')
                else:
                    os.system('sh startup.sh')
                break
        current_app.logger.info(f'启动{v}tomcat服务成功')
        return f'启动{v}tomcat服务成功'

    def renameProductJar(self,newName,path):
        jar_list=os.listdir(path)
        for i in jar_list:
            if newName.split('.')[0] in i.split('.')[0]:
                os.rename(f'{path}/{i}',f'{path}/{newName}')

    def copy_Jar(self,to_path_in, version):
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
            from_path_in = f'{self.ip}{version}'
        else:
            from_path_in = f'{self.ip}{version}'
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
                    self.renameProductJar(file_name,os.path.join(to_path_in, "product"))
                backup_file = os.path.join(backup_path, file_name)
                ubuntu_file = os.path.join(self.config[version][2], file_name)
                try:
                    from_134_file = from_file.replace(self.ip, self.ip_134)
                    if not filecmp.cmp(from_file, from_134_file):
                        from_file = from_134_file
                    if not filecmp.cmp(from_file, to_file):
                        # current_app.logger.info(f'{version}有新的{file_name}\n')
                        # log += f'{version}有新的{file_name}\n'
                        # print(version + "有新的" + file_name, end='...\n')
                        # copy2(to_file, backup_file)
                        copy2(from_file, to_file)
                        copy2(from_file, ubuntu_file)
                        current_app.logger.info(f"{file_name}更新完毕,时间：{self.current_time()}\n")
                        log += f"{file_name}更新完毕,时间：{self.current_time()}\n"
                        print(f"{file_name}更新完毕,时间：{self.current_time()}\n")
                        flag = 1
                except PermissionError:
                    current_app.logger.info(f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}")
                    log += f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}"
                    print(f"{path}下{file_name}正在被占用，请稍等...time{self.current_time()}\n")
            # if flag == 1:
            # clean_jar(to_path_in)
        except FileNotFoundError as err:
            current_app.logger.info(f'file error:{err}\n')
            log += f'\nfile error:{err}'
            print(f'\nfile error:{err}')
        return log


    def copy_and_reload(self,v):
        """
        :param v: 版本号 develop
        :return:
        """
        log = '<p>'
        version = v
        v = self.ip + v + '/'
        log += f'{self.current_time()}</p><p>'
        # index = from_path.index(v)
        # clean_jar(to_path[index] + path)
        # 先关闭tomcat，然后换JAR，再启动tomcat
        log += self.shut_tomcat(version)
        log += self.copy_Jar(self.config[version][0] + self.YongHong_path, version)
        log += self.start_tomcat(version)
        return f'{log}检查完毕'


    def new_copy(self,v):
        """
        :param v: 版本号 develop
        :return:
        """
        log = ''
        version = v
        v = self.ip + v + '/'
        log += f'{self.current_time()}'
        # index = from_path.index(v)
        # print('清理备份的jar')
        # log += '清理备份的jar'
        # clean_jar(to_path[index] + path)
        # work_dir = to_path[index] + tomcat_path
        # host_port = eval(port[index])
        # os.chdir(work_dir)
        # 先关闭tomcat，然后换JAR，再启动tomcat
        log += self.copy_Jar(self.config[version][0] + self.YongHong_path, version)
        current_app.logger.info(f'{v}最新包检查完毕')
        return f'{log}检查完毕'
