import os
import time
from shutil import copy2, rmtree
import filecmp


def copy_Jar(from_path, to_path):
    log = ''
    try:
        path0 = time.strftime("%Y%m%d", time.localtime())
        backup_path = to_path + '/backup_product'
        path = from_path + path0
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
            to_file = to_path + "/product/" + file_name
            backup_file = backup_path + "/" + file_name
            try:
                if not filecmp.cmp(from_file, to_file):
                    log += from_path.split('/')[1] + "有新的" + file_name +'</p><p>'
                    print(from_path.split('/')[1] + "有新的" + file_name, end='...')
                    copy2(to_file, backup_file)
                    copy2(from_file, to_file)
                    log += "更新完毕,时间：" + time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
                    print("更新完毕,时间：", time.strftime("%H:%M:%S", time.localtime()))
            except PermissionError:
                log += path + "下" + file_name + "正在被占用，请稍等...time:" + time.strftime("%H:%M:%S", time.localtime()) +'</p><p>'
                print(path + "下", file_name, "正在被占用，请稍等...time:" + time.strftime("%H:%M:%S", time.localtime()))
    except FileNotFoundError as err:
        log += '\nfile error:{0}'.format(err) +'</p><p>'
        print('\nfile error:{0}'.format(err))
    return log


def clean_jar(path):
    back_path = path + '/backup_product'
    rmtree(back_path)
