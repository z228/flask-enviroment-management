from json import loads, dumps
from os import listdir
from os.path import join

from apps.lib.FtpServer import MyFTP
from flask import Blueprint, request, render_template
from functools import wraps

from . import test
from .product import ProductAction

ALLOWED_EXTENSIONS = {'jar'}

productJar_operate = Blueprint('productJar', __name__)

productAction = ProductAction()
VERSION = list(productAction.config.keys())


# 定义鉴权装饰器，判断用户是否存在
def authentication_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 判断session是否保存了用户名，保存了即该用户已登录
        name = request.headers.get('Authorization')
        user = productAction.get_user_by_username(name)
        if user:
            return func(*args, *kwargs)
        return productAction.user_not_found(name)

    return wrapper


# 产品jar功能页面
@productJar_operate.route('/', methods=['POST', 'GET'])
def product():
    return render_template('product.html')


# 获取脚本列表
@productJar_operate.route('/allScript', methods=['GET'])
@authentication_user
def get_all_script():
    return productAction.succ(productAction.get_all_script())


# 执行脚本
@productJar_operate.route('/execute', methods=['post'])
def execute_script():
    data = loads(request.get_data())
    return productAction.succ(productAction.execute_script(data['name']))


# 删除脚本
@productJar_operate.route('/delete', methods=['post'])
def delete_script():
    data = loads(request.get_data())
    return productAction.succ(productAction.delete_script(data['name']))


# 保存脚本
@productJar_operate.route('/saveScript', methods=['post'])
def save_script():
    data = loads(request.get_data())
    return productAction.succ(productAction.save_script(data['content'], data['name'], data['type']))


# 获取所有版本号
@productJar_operate.route('/all', methods=['GET'])
@authentication_user
def get_all_version():
    v = {}
    for key in VERSION:
        v[key] = {}
        v[key]['path'] = productAction.config[key]["path"]
        v[key]['branch'] = productAction.config[key]["branch"]
    return productAction.succ(productAction.config)


# 获取所有bihome
@productJar_operate.route('/allBihome', methods=['GET'])
@authentication_user
def get_all_bihome():
    v = {key: productAction.config[key]["bihomes"].split(' ') for key in VERSION}
    # for key in VERSION:
    #     v[key] = productAction.config[key]["bihomes"].split(' ')
    return productAction.succ(v)


# 获取当前bihome
@productJar_operate.route('/currentBihome', methods=['GET'])
@authentication_user
def get_current_bihome():
    v = {key: productAction.config[key]["bihome"] for key in VERSION}
    # for key in VERSION:
    #     v[key] = productAction.config[key]["bihome"]
    return productAction.succ(v)


# jar包信息
@productJar_operate.route('/jarInfo', methods=['GET'])
@authentication_user
def get_product_jar_info():
    v = {key: productAction.get_jar_info(key) for key in VERSION}
    return productAction.succ(v)


# 获取141备份的jar包列表
@productJar_operate.route('/141jar', methods=['GET'])
@authentication_user
def get_141_jar():
    v = productAction.jar_list
    return productAction.succ(productAction.get_jar_list())


@productJar_operate.route('/releasejar', methods=['GET'])
@authentication_user
def get_release_jar():
    v = productAction.jar_list
    return productAction.succ(productAction.get_release_jar_list())


# 更换环境bihome
@productJar_operate.route('/changeBihome', methods=['POST'])
@authentication_user
def change_bihome():
    data = loads(request.get_data())
    return productAction.succ(productAction.change_bi_home(data['version'], data['bihome']))


# 停止产品
@productJar_operate.route('/shutdown', methods=['POST'])
@authentication_user
def shutdown_product():
    data = loads(request.get_data())
    return productAction.succ(productAction.shut_tomcat(data['version']))


# 启动产品
@productJar_operate.route('/startup', methods=['POST'])
@authentication_user
def start_product():
    data = loads(request.get_data())
    if 'user' in data.keys():
        res = productAction.start_tomcat(data['version'], data['user'])
        if '成功' not in res:
            return productAction.info(res)
        else:
            return productAction.succ(res)
    else:
        return productAction.succ(productAction.start_tomcat(data['version']))


# 检测产品是否启动中
@productJar_operate.route('/check', methods=['GET'])
@authentication_user
def check_product():
    v = {}
    for key in VERSION:
        v[key] = {}
        v[key]["startup"] = productAction.config[key]["startup"]
        v[key]["shutdown"] = productAction.config[key]["shutdown"]
        v[key]["update"] = productAction.config[key]["update"]
        v[key]["reload"] = productAction.config[key]["reload"]
        v[key]["updateAndReload"] = productAction.config[key]["updateAndReload"]
        v[key]["status"] = productAction.config[key]["status"]
    return productAction.succ(v)


# 获取debug端口
@productJar_operate.route('/port', methods=['GET'])
@authentication_user
def get_port():
    v = {key: productAction.config[key]["debug"] for key in VERSION}
    return productAction.succ(v)


# 获取产品端口
@productJar_operate.route('/bi', methods=['GET'])
@authentication_user
def get_view_port():
    v = {key: productAction.config[key]["port"] for key in VERSION}
    return productAction.succ(v)


# 更换Jar包
@productJar_operate.route('/update', methods=['POST'])
@authentication_user
def update_jar():
    data = loads(request.get_data())
    copy_release = data['copy_release'] if 'copy_release' in data.keys() else False
    release = data['release'] if 'release' in data.keys() else ''
    return productAction.succ(
        productAction.new_copy(data['version'], data['date'], copy_release, release))


# 更换指定日期Jar包
@productJar_operate.route('/updatewithDate', methods=['POST'])
@authentication_user
def update_jar_with_date():
    data = loads(request.get_data())
    return productAction.succ(productAction.new_copy(data['version'], data['date']))


# 更换Linux服务器Jar包
@productJar_operate.route('/updateLinuxJar', methods=['POST'])
def update_linux_jar():
    ftpServer = MyFTP()
    ftpServer.connect()
    ftpServer.login()
    data = loads(request.get_data())
    src_path = productAction.get_fast_path(data['version'])
    src_path = src_path.replace(productAction.ip, productAction.ip_134)
    key2 = "v9.4" if data['version'] == "v9.4.1" else data['version']
    if key2 in ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']:
        src_path = src_path.replace(productAction.ip_134, productAction.ip_187)
    dirs = listdir(src_path)
    for dir in dirs:
        src_file = join(src_path, dir)
        if dir.split('\\')[-1] not in productAction.yonghong_product_jar:
            continue
        src_file = join(src_path, dir)
        ftpServer.upload_file(src_file, f'/{data["version"]}')
    ftpServer.quit()
    return productAction.succ(f'服务器{data["version"]}的Jar包更新成功')


# 重启产品
@productJar_operate.route('/reload_product', methods=['POST'])
@authentication_user
def reload_product():
    data = loads(request.get_data())
    return productAction.succ(productAction.restart_tomcat(data['version']))


# 更换Jar包并重启产品
@productJar_operate.route('/updateReload', methods=['POST'])
@authentication_user
def update_and_reload_product():
    data = loads(request.get_data())
    copy_release = data['copy_release'] if 'copy_release' in data.keys() else False
    release = data['release'] if 'release' in data.keys() else ''
    return productAction.succ(
        productAction.copy_and_reload(data['version'], data['date'], copy_release, release))


# 获取当前bihome
@productJar_operate.route('/url', methods=['GET'])
@authentication_user
def get_url():
    v = {}
    for key in productAction.config.keys():
        v[key] = productAction.config[key]["url"]
    return productAction.succ(v)


# 登录系统校验
@productJar_operate.route('/login', methods=['POST'])
def login():
    data = loads(request.get_data())
    return productAction.user_validation(data)


# 更新用户信息
@productJar_operate.route('/updateuserinfo', methods=['POST'])
def update_userinfo():
    data = loads(request.get_data())
    print(data)
    return productAction.update_userinfo(data)


# 获取当前用户信息
@productJar_operate.route('/getuserinfo', methods=['POST'])
def get_userinfo():
    data = loads(request.get_data())
    username = data["username"]
    user = productAction.get_user_by_username(username)
    if user:
        return productAction.succ(user.get_info())
    return productAction.user_not_found(username)


# 添加用户
@productJar_operate.route('/adduser', methods=['POST'])
def add_user():
    data = loads(request.get_data())
    return productAction.create_new_user(data)


# 删除用户
@productJar_operate.route('/deleteuser', methods=['POST'])
def delete_user():
    data = loads(request.get_data())
    username = data["username"].strip().lower()
    return productAction.delete_user(username)


# junit需要更换exp的case
@productJar_operate.route('/junitexp', methods=['POST'])
@authentication_user
def get_junit_fail_list():
    data = loads(request.get_data())
    productAction.change_junit_exp(data)
    return productAction.succ("成功")


# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
    if request.method == 'POST':
        aim = request.form['exchange']
        log = productAction.new_copy(aim)
        return '''<link rel="shortcut icon" href="{{ url_for('static', 
        filename='favicon.ico') }}">''' + log + '''<script type="text/javascript">setTimeout("history.go(-1)", 3000);  </script>
            <SCRIPT language=javascript>
            function go()
            {
             window.history.go(-1);
            }
            setTimeout("go()",3000);
            </SCRIPT>'''
        # request.form.
    return render_template('exchange.html')


# 重启服务功能页面
@productJar_operate.route('/reload', methods=['POST', 'GET'])
def reload():
    if request.method == 'POST':
        aim = request.form['reload']
        # print(request.form['reload'])
        log = productAction.restart_tomcat(aim)
        return '''<link rel="shortcut icon" href="{{ url_for('static', 
        filename='favicon.ico') }}">''' + log + '''<script type="text/javascript">setTimeout("history.go(-1)", 3000);  </script>
            <SCRIPT language=javascript>
            function go()
            {
             window.history.go(-1);
            }
            setTimeout("go()",3000);
            </SCRIPT>'''
    return render_template('reload.html')


# 备份功能
@productJar_operate.route('/backup', methods=['POST', 'GET'])
def backup():
    if request.method == 'POST':
        aim = request.form['backup']
        # print(request.form['backup'])
        if aim == '还原':
            flag = test.revert_bi_home()
        elif aim == 'trunkJunit更换':
            flag = test.exchange_junit_res()
        else:
            flag = test.copy_db_to_bi_home(test.path[aim])
        if flag:
            return '备份或还原成功'
    return render_template('backup.html')
