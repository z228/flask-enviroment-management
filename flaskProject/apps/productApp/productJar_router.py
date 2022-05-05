from time import perf_counter, sleep
from flask import Blueprint, request, render_template
from .product import ProductAction
import json
from . import test
from .status import toked
import os
from apps.lib.FtpServer import MyFTP

productJar_operate = Blueprint('productJar', __name__)

productAction = ProductAction()


# 产品jar功能页面
@productJar_operate.route('/', methods=['POST', 'GET'])
def product():
    return render_template('product.html')


# 获取脚本列表
@productJar_operate.route('/allScript', methods=['GET'])
def get_all_script():
    # productAction = ProductAction()
    return productAction.succ(productAction.get_all_script())


# 执行脚本
@productJar_operate.route('/execute', methods=['post'])
def execute_script():
    data = json.loads(request.get_data())
    # productAction = ProductAction()
    return productAction.succ(productAction.execute_script(data['name']))


# 删除脚本
@productJar_operate.route('/delete', methods=['post'])
def delete_script():
    data = json.loads(request.get_data())
    # productAction = ProductAction()
    return productAction.succ(productAction.delete_script(data['name']))


# 保存脚本
@productJar_operate.route('/saveScript', methods=['post'])
def save_script():
    data = json.loads(request.get_data())
    # productAction = ProductAction()
    return productAction.succ(productAction.save_script(data['content'], data['name'], data['type']))


# 获取所有版本号
@productJar_operate.route('/all', methods=['GET'])
def get_all_version():
    # productAction = ProductAction()
    v = {}
    for key in productAction.config.keys():
        v[key] = {}
        v[key]['path'] = productAction.config[key]["path"]
        v[key]['branch'] = productAction.config[key]["branch"]
    return productAction.succ(v)


# 获取所有bihome
@productJar_operate.route('/allBihome', methods=['GET'])
def get_all_bihome():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key]["bihomes"].split(' ')
    return productAction.succ(v)


# 获取当前bihome
@productJar_operate.route('/currentBihome', methods=['GET'])
def get_current_bihome():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key]["bihome"]
    return productAction.succ(v)


# 获取所有bihome
@productJar_operate.route('/jarInfo', methods=['GET'])
def get_product_jar_info():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.get_jar_info(key)
    return productAction.succ(v)


# 获取141备份的jar包列表
@productJar_operate.route('/141jar', methods=['GET'])
def get_141_jar():
    # v = {}
    # productAction = ProductAction()
    v = productAction.jar_list
    return productAction.succ(productAction.get_jar_list())


# 更换环境bihome
@productJar_operate.route('/changeBihome', methods=['POST'])
def change_bihome():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.change_bi_home(data['version'], data['bihome']))


# 停止产品
@productJar_operate.route('/shutdown', methods=['POST'])
def shutdown_product():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    print(data['version'])
    # return succ('关闭成功')
    return productAction.succ(productAction.shut_tomcat(data['version']))


# 启动产品
@productJar_operate.route('/startup', methods=['POST'])
def start_product():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
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
def check_product():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = {}
        v[key]["startup"] = productAction.config[key]["startup"]
        v[key]["shutdown"] = productAction.config[key]["shutdown"]
        v[key]["update"] = productAction.config[key]["update"]
        v[key]["reload"] = productAction.config[key]["reload"]
        v[key]["updateAndReload"] = productAction.config[key]["updateAndReload"]
    return productAction.succ(v)


# 获取debug端口
@productJar_operate.route('/port', methods=['GET'])
def get_port():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.get_debug_port(key)
    return productAction.succ(v)


# 获取产品端口
@productJar_operate.route('/bi', methods=['GET'])
def get_view_port():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.get_bi_port(key)
    return productAction.succ(v)


# 更换Jar包
@productJar_operate.route('/update', methods=['POST'])
def update_jar():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.new_copy(data['version'], data['date']))


# 更换指定日期Jar包
@productJar_operate.route('/updatewithDate', methods=['POST'])
def update_jar_with_date():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.new_copy(data['version'], data['date']))


# 更换Linux服务器Jar包
@productJar_operate.route('/updateLinuxJar', methods=['POST'])
def update_linux_jar():
    # productAction = ProductAction()
    ftpServer = MyFTP()
    ftpServer.connect()
    ftpServer.login()
    data = json.loads(request.get_data())
    src_path = productAction.get_recent_jar(data['version'])
    src_path = src_path.replace(productAction.ip, productAction.ip_134)
    key2 = "v9.4" if data['version'] == "v9.4.1" else data['version']
    if key2 in ['v8.6', 'v9.0', 'v9.2.1', 'v9.4', 'develop']:
        src_path = src_path.replace(productAction.ip_134, productAction.ip_187)
    dirs = os.listdir(src_path)
    for dir in dirs:
        src_file = os.path.join(src_path, dir)
        if dir.split('\\')[-1] not in ['api.jar', 'product.jar', 'thirds.jar']:
            continue
        src_file = os.path.join(src_path, dir)
        ftpServer.upload_file(src_file, f'/{data["version"]}')
    ftpServer.quit()
    return productAction.succ(f'服务器{data["version"]}的Jar包更新成功')


# 重启产品
@productJar_operate.route('/reload_product', methods=['POST'])
def reload_product():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.restart_tomcat(data['version']))


# 更换Jar包并重启产品
@productJar_operate.route('/updateReload', methods=['POST'])
def update_and_reload_product():
    # productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.copy_and_reload(data['version'], data['date']))


# 获取当前bihome
@productJar_operate.route('/url', methods=['GET'])
def get_url():
    v = {}
    # productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key]["url"]
    return productAction.succ(v)


# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
    # productAction = ProductAction()
    if request.method == 'POST':
        aim = request.form['exchange']
        print(request.form['exchange'])
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
    # productAction = ProductAction()
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
    # productAction = ProductAction()
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
