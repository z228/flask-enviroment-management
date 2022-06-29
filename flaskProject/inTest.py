from filecmp import cmpfiles
import json
from time import time
import os
from filecmp import cmp
from apps.productApp.send_mail import send
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

patha = r'\\192.168.0.187\share\develop\20220527'
pathb = r'\\192.168.1.134\git-package\develop\20220527'
common = ['api.jar', 'product.jar', 'thirds.jar']
# res = cmpfiles(patha, pathb, common)

filea = r'\\192.168.1.199\jacoco\trunk\manual\backup\jacoco_20220606_zengchenglong3.exec'
fileb = r'D:\share\jacoco\trunk\jacoco_20220606_zengchenglong3.exec'

# print(cmp(filea, fileb))
subject = "jacoco上传结果通知"
sha256_filea = os.popen(f'certutil -hashfile {filea} SHA256').read()
sha256_fileb = os.popen(f'certutil -hashfile {fileb} SHA256').read()
content = f"199的jacoco SHA256：{sha256_filea}\n 本地jacoco SHA256:{sha256_fileb}"
send("zengchenglong@yonghongtech.com", subject, content)
# print(res)
