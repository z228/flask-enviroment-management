import os
from time import sleep

# work_dir = 'D:/old version/9.2/'
path = 'Yonghong Z-Suite/tomcat/bin'
_dir = []


def restart_tomcat(space):
    space = 'Z:/' + space + '/'
    from_path = ['Z:/v8.6/', 'Z:/v8.8/', 'Z:/v9.0/',
                 'Z:/v9.1/', 'Z:/v9.2/', 'Z:/develop/']
    index = from_path.index(space)
    _dir.append('D:/old version/8.6/')
    _dir.append('D:/old version/8.8/')
    _dir.append('D:/old version/9.0/')
    _dir.append('D:/old version/9.1/')
    _dir.append('D:/old version/9.2/')
    _dir.append('C:/')
    os.system("taskkill /F /IM java.exe")
    work_dir = _dir[index] + path
    os.chdir(work_dir)
    # os.system('shutdown')
    # sleep(15)
    os.system('startup')
    return '<p>重启完毕</p>'
