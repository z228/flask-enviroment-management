from .action_JAR import copy_Jar, clean_jar
import time


def new_copy(v):
    log = '<p>'
    v = 'Z:/' + v + '/'
    from_path = ['Z:/v8.6/', 'Z:/v8.8/', 'Z:/v9.0/',
                 'Z:/v9.1/', 'Z:/v9.2/', 'Z:/develop/']
    to_path = ['D:/old version/8.6/', 'D:/old version/8.8/', 'D:/old version/9.0/', 'D:/old version/9.1/',
               'D:/old version/9.2/', 'C:/']
    path = 'Yonghong Z-Suite/Yonghong'
    tomcat_path = 'Yonghong Z-Suite/tomcat/bin/'
    log += time.strftime("%H:%M:%S", time.localtime()) + '</p><p>'
    index = from_path.index(v)
    print('清理备份的jar')
    log += '清理备份的jar' + '</p><p>'
    clean_jar(to_path[index] + path)
    log += copy_Jar(from_path[index], to_path[index] + path)
    return log + '</p>'
