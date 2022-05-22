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

# res = os.popen('netstat -ano |findstr 8080').read()
# if "LISTENING" in res:
  # print(res)

jacoco_199_path = r'\\192.168.1.199\jacoco\trunk\manual'

jacoco_path = r'D:\jacoco'
os.chdir(jacoco_path)
jacoco_backup_files = [i.replace('\n','') for i in os.popen(f'dir /b {jacoco_199_path}\\backup').readlines() if "." in i]
jacoco_files = [i.replace('\n','') for i in os.popen(f'dir /b {jacoco_199_path}').readlines() if "." in i]
jacoco_files.extend(jacoco_backup_files)


def get_jacoco_files_list(path):
    jacoco_files = [i.replace('\n','') for i in os.popen(f'dir /b {path}').readlines() if ".exec" in i]
    return jacoco_files

jacoco_local_files= get_jacoco_files_list(r'D:\jacoco\trunk')

for jacoco in jacoco_local_files:
  if jacoco =="jacoco_${DATE}_all.exec":
    continue
  print(jacoco)
