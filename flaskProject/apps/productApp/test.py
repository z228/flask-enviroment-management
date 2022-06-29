import os
import shutil
import time
from logging import getLogger

product_logger = getLogger("product")

path = {
    'back_up_folder_name': r'D:\old_version\trunk\Yonghong_Z-Suite\Yonghong',
    'junit': r'D:\\SVN\\trunk\\test\\assetExecute\\work\\DBPainter',
    'UiAuto': r'D:\\SVN\trunk\test\YHAuto\\TestData\\DB\\Common'
}
bi_home = r'D:\old_version\trunk\\Yonghong_Z-Suite\\Yonghong\bihome'
back_up_folder_name = r'C:\\Yonghong_Z-Suite\\Yonghong\\' + 'bihome_' + time.strftime("%Y_%m_%d", time.localtime())
date_img = ['assetExecute/testcases/DBPainter/exp/Tab/properties/padding__日期过滤1__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/padding__选项卡6__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤1__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤2__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤3__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤4__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤5__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤6__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤7__RT.png',
            'assetExecute/testcases/DBPainter/exp/Tab/properties/positionType__日期过滤8__RT.png',
            'assetExecute/testcases/DBPainter/exp/Carousel/elemsFilt.pdf'
            ]
dist_list = ['v8.6_test','v9.0_test','v9.2.1_test','v9.4_test','trunk_test']
aim_list = ['branch/v8.6','branch/v9.0','branch/v9.2.1','branch/v9.4','trunk']


def exchange_junit_res():
    for i in range(len(dist_list)):
        for img_path in date_img:
            if dist_list[i] =='v8.6_test' and 'Carousel' in img_path:
                continue
            dist = f'\\\\192.168.1.199/{dist_list[i]}/' + img_path.replace('exp', 'res')
            aim = f'D:/SVN/{aim_list[i]}/test/' + img_path
            # aim = f'\\\\192.168.1.199/{dist_list[i]}/' + img_path
            current_app.logger.info(dist)
            if "v9.4" or "trunk" in aim_list[i] and "elemsFilt" in img_path:
                continue
            shutil.copy2(dist, aim)
        # SVN_dir = f'\\\\192.168.1.199/{dist_list[i]}/assetExecute/testcases/DBPainter/exp'
        SVN_dir = f'D:/SVN/{aim_list[i]}/test/assetExecute/testcases/DBPainter/exp'
        print(SVN_dir)
        product_logger.info(SVN_dir)
        os.system(f'svn update {SVN_dir}')
        os.system(f'svn commit {SVN_dir} -m "dateElem change" > {os.getcwd()}/logs/SVN_logs/SVN_{dist_list[i]}_Commit.txt')
    return True


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
        os.mkdir(bi_home, 0o777)
        raise Exception('%s is not exist, now make it, please try again!' % bi_home)


def copy_db_to_bi_home(new_bi_home_folder_path):
    if os.path.exists(new_bi_home_folder_path):
        _back_up_bi_home()
        shutil.rmtree(bi_home)
        shutil.copytree(new_bi_home_folder_path, bi_home)
        print(u'DB拷贝成功')
        return True
    else:
        raise Exception('%s is not exist, now make it, please try again!' % new_bi_home_folder_path)
