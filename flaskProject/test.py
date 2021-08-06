import os
import shutil
import time

path = {
    'back_up_folder_name': r'D:\old_version\trunk\Yonghong_Z-Suite\Yonghong',
    'junit': r'D:\\SVN\\trunk\\test\\assetExecute\\work\\DBPainter',
    'UiAuto': r'D:\\SVN\trunk\test\YHAuto\\TestData\\DB\\Common'
}
bi_home = r'D:\old_version\trunk\\Yonghong_Z-Suite\\Yonghong\bihome'
back_up_folder_name = r'C:\\Yonghong_Z-Suite\\Yonghong\\' + 'bihome_' + time.strftime("%Y_%m_%d", time.localtime())


def _back_up_bi_home():
    if os.path.exists(bi_home):
        if os.path.exists(back_up_folder_name):
            shutil.rmtree(back_up_folder_name)
            # 兼容多bi_home配置，不直接删除备份，而是将备份存储到一个带有时间戳的bihome里。
        shutil.copytree(bi_home, back_up_folder_name)
        print(u'bihome 备份完成')
        return True
    else:
        os.mkdir(bi_home, 0o777)
        raise Exception('%s is not exist, now make it, please check!' % bi_home)


def revert_bi_home():
    if os.path.exists(bi_home):
        shutil.rmtree(bi_home)
        shutil.copytree(back_up_folder_name, bi_home)
        # shutil.rmtree(back_up_folder_name)
        print(u'bihome 恢复完成')
        return True
    else:
        os.mkdir(self.bi_home, 0o777)
        raise Exception('%s is not exist, now make it, please try again!' % self.bi_home)


def copy_db_to_bi_home(new_bi_home_folder_path):
    if os.path.exists(new_bi_home_folder_path):
        _back_up_bi_home()
        shutil.rmtree(bi_home)
        shutil.copytree(new_bi_home_folder_path, bi_home)
        print(u'DB拷贝成功')
        return True
    else:
        raise Exception('%s is not exist, now make it, please try again!' % new_bi_home_folder_path)
