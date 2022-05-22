import redis

# 获取redis数据库连接
# r = redis.StrictRedis(host="192.168.0.187", port=6379, db=0)
#
# # redis存入键值对
# r.set(name="key", value="value")
# # 读取键值对
# print(r.get("key"))

from os import getcwd
from json import load

with open(f'{getcwd()}/apps/productApp/user.json', 'r', encoding='utf-8') as user:
    user_list = load(user)
    print(user_list['zcl'])
