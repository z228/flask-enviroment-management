import os


def static_clean():
    print('clean---')
    for f in os.listdir('static/results'):
        print('删除文件' + f)
        os.remove('./static/results/' + f)
    for f in os.listdir('./static/uploads'):
        print('删除文件' + f)
        os.remove('./static/uploads/' + f)
