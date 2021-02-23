import os


def static_clean():
    print('clean---')
    for f in os.listdir('./static/result'):
        print('删除文件' + f)
        os.remove('./static/result/' + f)
