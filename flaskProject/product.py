import os
import time
from shutil import copy2, rmtree
import filecmp
import socket

ip = '\\\\192.168.0.141/productJar/'
# ip = '\\\\192.168.1.134/git-package/'
from_path = [ip + 'v8.6/', ip + 'v8.8/', ip + 'v9.0/', ip +
             'v9.1/', ip + 'v9.2/', ip + 'v9.2.1/', ip + 'develop/']
to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'C:/']
day_31 = ['02', '04', '06', '08', '09', '11']
port = ['8086', '', '8090', '8091', '8092', '8921', '8080']


def is_port_used(ip, port):
    """
    check whether the port is used by other program
    检测端口是否被占用

    :param ip:
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def restart_tomcat(v):
    host_ip = '127.0.0.1'
    version = v
    log = '<p>'
    v = ip + v + '/'
    path = 'Yonghong_Z-Suite/Yonghong'
    tomcat_path = 'Yonghong_Z-Suite/tomcat/bin/'
    log += time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
    index = from_path.index(v)
    # print('清理备份的jar')
    # log += '清理备份的jar' + '</p><p>'
    # clean_jar(to_path[index] + path)
    host_port = eval(port[index])

    work_dir = to_path[index]+tomcat_path
    os.chdir(work_dir)
    # 判断tomcat是否是启动状态
    if(is_port_used(host_ip, host_port)):
        os.system('shutdown')
        log += '停止tomcat服务' + '</p><p>'
    else:
        log += 'tomcat服务未启动' + '</p><p>'
    log += copy_Jar(from_path[index], to_path[index] + path,version)
    for i in range(100):
        if(is_port_used(host_ip, host_port)):
            time.sleep(10)
        else:
            os.system('startup')
            break
    log += '重启tomcat服务成功' + '</p><p>'
    return log + '</p><p>检查完毕</p>'


def copy_Jar(from_path_in, to_path_in, version):
    log = ''
    flag = 0
    try:
        path0 = time.strftime("%Y%m%d", time.localtime())
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not os.path.exists(from_path_in + path0):
                if path0[-2:] == '01':
                    if path0[5:6] in day_31:
                        path0 = path0[0:5] + str(eval(path0[5:6]) - 1) + '31'
                    elif eval(path0[5:6]) - 1 == 2 and eval(path0[0:4]) % 4 == 0:
                        path0 = path0[0:5] + str(eval(path0[5:6]) - 1) + '29'
                    elif eval(path0[5:6]) - 1 == 2 and eval(path0[0:4]) % 4 != 0:
                        path0 = path0[0:5] + str(eval(path0[5:6]) - 1) + '28'
                    elif path0[4:6] == '01':
                        path0 = str(eval(path0[0:4]) - 1) + '1231'
                    else:
                        path0 = path0[0:5] + str(eval(path0[5:6]) - 1) + '30'
                else:
                    path0 = str(eval(path0) - 1)
            else:
                break
        log += path0 + '的包</p><p>'
        backup_path = to_path_in + '/backup_product'
        path = from_path_in + path0
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
            from_file = path + "/" + file_name
            to_file = to_path_in + "/product/" + file_name
            backup_file = backup_path + "/" + file_name
            try:
                if not filecmp.cmp(from_file, to_file):
                    log += version + "有新的" + file_name + '</p><p>'
                    print(version + "有新的" + file_name, end='...')
                    copy2(to_file, backup_file)
                    copy2(from_file, to_file)
                    log += "更新完毕,时间：" + \
                        time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
                    print("更新完毕,时间：", time.strftime(
                        "%H:%M:%S", time.localtime()))
                    flag = 1
            except PermissionError:
                log += path + "下" + file_name + "正在被占用，请稍等...time:" + time.strftime("%H:%M:%S",
                                                                                    time.localtime()) + '</p><p>'
                print(path + "下", file_name, "正在被占用，请稍等...time:" +
                      time.strftime("%H:%M:%S", time.localtime()))
        # if flag == 1:
            # clean_jar(to_path_in)
    except FileNotFoundError as err:
        log += '\nfile error:{0}'.format(err) + '</p><p>'
        print('\nfile error:{0}'.format(err))
    return log





def new_copy(v):
    log = '<p>'
    v = ip + v + '/'
    path = 'Yonghong_Z-Suite/Yonghong'
    tomcat_path = 'Yonghong_Z-Suite/tomcat/bin/'
    log += time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
    index = from_path.index(v)
    print('清理备份的jar')
    log += '清理备份的jar' + '</p><p>'
    clean_jar(to_path[index] + path)
    log += copy_Jar(from_path[index], to_path[index] + path, v)
    return log + '</p><p>检查完毕</p>'
