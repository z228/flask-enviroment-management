from json import loads, load
from os import listdir
from os.path import join, exists
from shutil import copy2

from flask import Blueprint, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from functools import wraps

from . import test
from .product import ProductAction
from .junit import *
from .task import jar_list

ALLOWED_EXTENSIONS = {'jar'}

productJar_operate = Blueprint('productJar', __name__)
product_logger = getLogger("product")
junit_logger = getLogger("junit")
productAction = ProductAction()
VERSION = list(productAction.config.keys())


# 定义鉴权装饰器，判断用户是否存在
def authentication_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 判断session是否保存了用户名，保存了即该用户已登录
        name = request.headers.get('Authorization')
        if name:
            username = name.strip().lower()
            user = productAction.get_user_by_username(username)
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
    # v = {}
    # for key in VERSION:
    #     v[key] = productAction.config[key]
    #     v[key]["startUser"] = productAction.config[key]["startUser"] if productAction.is_port_used_fast(
    #         productAction.config[key]["port"]) else '0'
    return productAction.succ(VERSION)


# 获取所有bihome
@productJar_operate.route('/allBihome', methods=['GET'])
@authentication_user
def get_all_bihome():
    v = {key: productAction.config[key]
         ["bihomes"].split(' ') for key in VERSION}
    return productAction.succ(v)


# 获取当前bihome
@productJar_operate.route('/currentBihome', methods=['GET'])
@authentication_user
def get_current_bihome():
    v = {key: productAction.config[key]["bihome"] for key in VERSION}
    return productAction.succ(v)


# 获取所有jar包信息
@productJar_operate.route('/jarInfo', methods=['GET'])
@authentication_user
def get_product_jar_info():
    v = {key: productAction.get_jar_info(key) for key in VERSION}
    return productAction.succ(v)


# 获取bi.properties内容
@productJar_operate.route('/biPro', methods=['GET'])
@authentication_user
def get_product_bi_properties():
    v = {key: productAction.get_bi_properties(key) for key in VERSION}
    return productAction.succ(v)


# 获取当前url
@productJar_operate.route('/url', methods=['GET'])
@authentication_user
def get_url():
    v = {key: productAction.config[key]["url"] for key in VERSION}
    return productAction.succ(v)


# 获取141备份的jar包列表
@productJar_operate.route('/141jar', methods=['GET'])
@authentication_user
def get_141_jar():
    # v = productAction.get_jar_list()
    # product_logger.info(jar_list)
    return productAction.succ(jar_list)


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
    print(data['version'])
    res = productAction.shut_tomcat(data['version'], data['user'])
    return productAction.info(res) if '成功' not in res else productAction.succ(res)


# 启动产品
@productJar_operate.route('/startup', methods=['POST'])
@authentication_user
def start_product():
    data = loads(request.get_data())
    res = productAction.start_tomcat(data['version'], data['user'])
    return productAction.succ(res) if '成功' in res else productAction.info(res)


# 检测产品是否启动中
@productJar_operate.route('/check', methods=['GET'])
@authentication_user
def check_product():
    v = {}
    for key in VERSION:
        v[key] = productAction.config[key]
        v[key]["startUser"] = productAction.config[key]["startUser"] if productAction.is_port_used_fast(
            productAction.config[key]["port"]) else '0'
        v[key]["startup"] = productAction.config[key]["startup"]
        v[key]["shutdown"] = productAction.config[key]["shutdown"]
        v[key]["update"] = productAction.config[key]["update"]
        v[key]["reload"] = productAction.config[key]["reload"]
        v[key]["updateAndReload"] = productAction.config[key]["updateAndReload"]
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
    res = productAction.copy_jar(data['version'], data['date'], data['user'])
    return productAction.succ(res) if '完成' in res else productAction.info(res)


# 更换指定日期Jar包
@productJar_operate.route('/updatewithDate', methods=['POST'])
@authentication_user
def update_jar_with_date():
    data = loads(request.get_data())
    res = productAction.copy_jar(data['version'], data['date'], data['user'])
    return productAction.succ(res) if '完成' in res else productAction.info(res)


def allowed_file(filename):
    """
    检验文件名尾缀是否满足格式要求
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 上传ar包
@productJar_operate.route('/uploadJar', methods=['POST'])
def upload_jar():
    version = request.form.get('version')
    user = request.form.get('user')
    check_res = productAction.check_status(version)
    if check_res != '0':
        return productAction.info(check_res)
    productAction.change_status(version, "update", True, user)
    file = request.files['file']
    if 'file' not in request.files:
        productAction.change_status(version, "update")
        return productAction.error("No file part")
    if file.filename == '':
        productAction.change_status(version, "update")
        return productAction.error('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if 'api' in filename:
            filename = 'api.jar'
        elif 'product' in filename:
            filename = 'product.jar'
        elif 'thirds' in filename:
            filename = 'thirds.jar'
        elif 'product-swf' in filename:
            filename = 'product-swf.jar'
        jar_path = productAction.config[version]["path"] + '/Yonghong/product'
        file.save(join(jar_path, filename))
        productAction.change_status(version, "update")
        return productAction.succ(f'{file.filename} uploaded successfully')
    productAction.change_status(version, "update")
    return productAction.error("file uploaded Fail")


# 重启产品
@productJar_operate.route('/reload_product', methods=['POST'])
@authentication_user
def reload_product():
    data = loads(request.get_data())
    res = productAction.restart_tomcat(data['version'], data['user'])
    return productAction.succ(res) if '成功' in res else productAction.info(res)


# 更换Jar包并重启产品
@productJar_operate.route('/updateReload', methods=['POST'])
@authentication_user
def update_and_reload_product():
    data = loads(request.get_data())
    res = productAction.copy_and_reload(
        data['version'], data['date'], data['user'])
    return productAction.succ(res) if '成功' in res else productAction.info(res)


# 登录系统校验
@productJar_operate.route('/login', methods=['POST'])
def login():
    data = loads(request.get_data())
    return productAction.user_validation(data)


# 更新用户信息
@productJar_operate.route('/updateuserinfo', methods=['POST'])
def update_userinfo():
    userinfo = loads(request.get_data())
    return productAction.update_userinfo(userinfo)


# 获取当前用户信息
@productJar_operate.route('/getuserinfo', methods=['POST'])
def get_userinfo():
    data = loads(request.get_data())
    username = data["username"]
    user = productAction.get_user_by_username(username)
    if user:
        return productAction.succ(user.getInfo())
    return productAction.user_not_found(username)


# 获取所有用户信息
@productJar_operate.route('/alluserinfo', methods=['GET'])
def get_all_userinfo():
    rep = []
    for user in productAction.users:
        rep.append(user.getInfo())
    return productAction.succ(rep)


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


@productJar_operate.route('/junitdiff', methods=['POST'])
@authentication_user
def get_junit_fail_list():
    data = loads(request.get_data())
    version = data["version"]
    with open(f'/home/share/junit_res/el_tree_{version}_test_res.json', 'r', encoding='utf-8') as f:
        fail_cases = load(f)
    return productAction.succ(fail_cases)


@productJar_operate.route('/junitexp', methods=['POST'])
@authentication_user
def exchange_junit_exp():
    data = loads(request.get_data())
    exp_path = f'/mnt/192/junit_test/{data["version"]}_test/assetExecute/testcases'
    for case in data["cases"]:
        src = join(exp_path, case)
        dst = src.replace('res', 'exp')
        copy2(src, dst)
    junit_logger.info(f'[{data["user"]}]-{data["cases"]} exchanged')
    return productAction.succ("更换成功")


@productJar_operate.route('/junitdisexp', methods=['POST'])
@authentication_user
def exchange_junit_dis_exp():
    data = loads(request.get_data())
    exp_path = f'/mnt/192/junit_test/{data["version"]}_test/assetExecute/testcases'
    for case in data["cases"]:
        src = join(exp_path, case)
        dst = src.replace('res', 'exp_dis')
        copy2(src, dst)
    junit_logger.info(f'[{data["user"]}]-{data["cases"]} exchanged')
    return productAction.succ("更换成功")


# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
    if request.method == 'POST':
        aim = request.form['exchange']
        print(request.form['exchange'])
        log = productAction.copy_and_reload(aim)
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
        print(request.form['reload'])
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


# 视频组件，返回视频流测试
@productJar_operate.route('/video/<name>', methods=['GET'])
def videoComponentTest(name=None):
    filePath = r'/home/share/video'
    if exists(join(filePath, name)):
        return send_from_directory(directory=filePath, path=name, as_attachment=False)
    return productAction.error("视频不存在")
