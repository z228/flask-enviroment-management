import os
import time
from shutil import copy2, rmtree
import filecmp

ip = '\\\\192.168.0.141/productJar/'
from_path = [ip + 'v8.6/', ip + 'v8.8/', ip + 'v9.0/', ip + 'v9.1/', ip + 'v9.2/', ip + 'v9.2.1/', ip + 'develop/']
to_path = ['D:/old version/8.6/', 'D:/old version/8.8/', 'D:/old version/9.0/', 'D:/old version/9.1/',
           'D:/old version/9.2/', 'D:/old version/9.2.1/', 'C:/']
day_31 = ['01', '03', '05', '07', '08', '10', '12']


def restart_tomcat(space):
    path = 'Yonghong Z-Suite/tomcat/bin'
    space = ip + space + '/'
    index = from_path.index(space)
    # os.system("taskkill /F /IM java.exe")
    work_dir = to_path[index] + path
    os.chdir(work_dir)
    os.system('shutdown')
    time.sleep(30)
    os.system('startup')
    return '<p>重启完毕</p>'


def copy_Jar(from_path_in, to_path_in):
    log = ''
    try:
        path0 = time.strftime("%Y%m%d", time.localtime())
        # 检测是否有当天的新Jar，否则往前推一天
        while 1:
            if not os.path.exists(from_path_in + path0):
                if path0[-2:] == '01':
                    if str(eval(path0[-4:-2]) - 1) in day_31:
                        path0 = path0[0:4] + str(eval(path0[-4:-2]) - 1) + '31'
                    elif str(eval(path0[-4:-2]) - 1)=='02':
                        path0 = path0[0:4] + str(eval(path0[-4:-2]) - 1) + '28'
                    else:
                        path0 = path0[0:4] + str(eval(path0[-4:-2]) - 1) + '30'
                else:
                    path0 = str(eval(path0) - 1)
            else:
                break
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
                    log += from_path_in.split('/')[1] + "有新的" + file_name + '</p><p>'
                    print(from_path_in.split('/')[1] + "有新的" + file_name, end='...')
                    copy2(to_file, backup_file)
                    copy2(from_file, to_file)
                    log += "更新完毕,时间：" + time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
                    print("更新完毕,时间：", time.strftime("%H:%M:%S", time.localtime()))
            except PermissionError:
                log += path + "下" + file_name + "正在被占用，请稍等...time:" + time.strftime("%H:%M:%S",
                                                                                    time.localtime()) + '</p><p>'
                print(path + "下", file_name, "正在被占用，请稍等...time:" + time.strftime("%H:%M:%S", time.localtime()))
    except FileNotFoundError as err:
        log += '\nfile error:{0}'.format(err) + '</p><p>'
        print('\nfile error:{0}'.format(err))
    return log


def clean_jar(path):
    back_path = path + '/backup_product'
    rmtree(back_path)


def new_copy(v):
    log = '<p>'
    v = ip + v + '/'
    path = 'Yonghong Z-Suite/Yonghong'
    tomcat_path = 'Yonghong Z-Suite/tomcat/bin/'
    log += time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
    index = from_path.index(v)
    # print('清理备份的jar')
    # log += '清理备份的jar' + '</p><p>'
    # clean_jar(to_path[index] + path)
    log += copy_Jar(from_path[index], to_path[index] + path)
    return log + '</p><p>检查完毕</p>'
