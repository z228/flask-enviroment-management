import os
import product

to_path = ['D:/old_version/8.6/', 'D:/old_version/8.8/', 'D:/old_version/9.0/', 'D:/old_version/9.1/',
           'D:/old_version/9.2/', 'D:/old_version/9.2.1/', 'C:/']
path = 'Yonghong_Z-Suite/Yonghong'

def clean_jar():
    for i in to_path:
        back_path = i + path + '/backup_product'
        rmtree(back_path)

def static_clean():
    print('clean---')
    for f in os.listdir('static/results'):
        print('删除文件' + f)
        os.remove('./static/results/' + f)
    for f in os.listdir('./static/uploads'):
        print('删除文件' + f)
        os.remove('./static/uploads/' + f)

def Jacoco_change_Jar():
    product.restart_tomcat('develop')
    work_dir = r'D:\SVN\trunk\test\assetExecute'
    os.chdir(work_dir)
    os.system('ant test report')