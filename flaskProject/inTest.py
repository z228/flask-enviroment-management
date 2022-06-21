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

x = "a"
patha = fr'\\192.168.0.187\{x}share\develop\20220527'
pathb = r'\\192.168.1.134\git-package\develop\20220527'
common = ['api.jar','product.jar','thirds.jar']
print(patha)