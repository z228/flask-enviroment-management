import json
from time import time
import os
# from product import new_copy
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET



ubuntu_path = [r'D:\ubuntu_wsl\rootfs\opt\productJar\8.6', r'D:\ubuntu_wsl\rootfs\opt\productJar\8.8',
               r'D:\ubuntu_wsl\rootfs\opt\productJar\9.0', r'D:\ubuntu_wsl\rootfs\opt\productJar\9.1',
               r'D:\ubuntu_wsl\rootfs\opt\productJar\9.2', r'D:\ubuntu_wsl\rootfs\opt\productJar\9.2.1',
               r'D:\ubuntu_wsl\rootfs\opt\productJar\9.3', r'D:\ubuntu_wsl\rootfs\opt\productJar\trunk']
ip = '\\\\192.168.0.141/productJar/'

date_img = ['trunk/test/DBPainter/exp/Tab/properties/padding__日期过滤1__RT.png]',
            'trunk/test/DBPainter/exp/Tab/properties/padding__选项卡6__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤1__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤2__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤3__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤4__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤5__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤6__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤7__RT.png',
            'trunk/test/DBPainter/exp/Tab/properties/positionType__日期过滤8__RT.png',
            'trunk/test/DBPainter/exp/Carousel/elemsFilt.pdf'
            ]

time_str = '20210819'
# print(time_str[0:4])
# print(time_str[4:6])
# print(time_str[-2:])
# print(os.listdir(r"D:\old_version\9.0\Yonghong_Z-Suite\Yonghong\product"))
def renameProductJar(newName,path):
    jar_list=os.listdir(path)
    for i in jar_list:
        if newName.split('.')[0] in i.split('.')[0]:
            pass
            # os.rename(f'{path}/{i}',f'{path}/{newName}')
# os.path.exists()

# renameProductJar('product.jar','D:\old_version\9.0\Yonghong_Z-Suite\Yonghong\product')
# print(os.listdir(r"D:\old_version\9.0\Yonghong_Z-Suite\Yonghong\product"))
# import  xml.dom.minidom

# file_path = r'D:\old_version\8.7\Yonghong_Z-Suite\tomcat\conf\server.xml'
# dom  = xml.dom.minidom.parse(file_path)
# root = dom.documentElement
# param = root.getElementsByTagName('Connector')
# # print(param)
# # entry = root.getElementsByTagName('env-entry-value')
# param_value = param[0].getAttribute('port')

# print(param_value)
# entry_value = entry[0].firstChild.data.split('\\')
# param_value[-1] = "bihome"
# entry_value[-1] = "bihome"
# param[0].firstChild.data = '\\'.join(param_value)
# entry[0].firstChild.data = '\\'.join(entry_value)

res = os.popen('netstat -ano |findstr 8080').read()
# if "LISTENING" in res:
  # print(res)

l2 = os.listdir('\\\\192.168.1.134\\git-package\V9.4')
l2.reverse()
print(l2)
l2.sort()
print(l2)