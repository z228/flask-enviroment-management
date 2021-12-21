from flask import Blueprint, request, redirect, render_template, url_for
from product import ProductAction
import json
import test

productJar_operate = Blueprint('productJar', __name__)

productAction = ProductAction()
productAction.readConfig()
# 产品jar功能页面
@productJar_operate.route('/', methods=['POST', 'GET'])
def product():
    return render_template('product.html')


# 获取脚本列表
@productJar_operate.route('/allScript', methods=['GET'])
def get_all_script():
    return productAction.succ(productAction.getAllScript())

# 执行脚本
@productJar_operate.route('/execute', methods=['post'])
def execute_script():
    data = json.loads(request.get_data())
    return productAction.succ(productAction.executeScript(data['name']))

# 删除脚本
@productJar_operate.route('/delete', methods=['post'])
def delete_script():
    data = json.loads(request.get_data())
    return productAction.succ(productAction.deleteScript(data['name']))


# 保存脚本
@productJar_operate.route('/saveScript', methods=['post'])
def save_script():
    data = json.loads(request.get_data())
    return productAction.succ(productAction.saveScript(data['content'], data['name'], data['type']))

# 获取所有版本号
@productJar_operate.route('/all', methods=['GET'])
def get_all_version():
    v = {}
    for key in productAction.config.keys():
        v[key] = productAction.config[key][0]
    return productAction.succ(v)

# 获取所有bihome
@productJar_operate.route('/allBihome', methods=['GET'])
def get_all_bihome():
    v = {}
    for key in productAction.config.keys():
        v[key] = productAction.config[key][3].split(' ')
    return productAction.succ(v)

#更换环境bihome
@productJar_operate.route('/changeBihome', methods=['POST'])
def change_bihome():
    data = json.loads(request.get_data())
    print(data)
    return productAction.succ(productAction.change_bi_home(data['version'],data['bihome']))

# 停止产品
@productJar_operate.route('/shutdown', methods=['POST'])
def shutdown_product():
    data = json.loads(request.get_data())
    print(data['version'])
    # return succ('关闭成功')
    return productAction.succ(productAction.shut_tomcat(data['version']))


# 启动产品
@productJar_operate.route('/startup', methods=['POST'])
def start_product():
    data = json.loads(request.get_data())

    return productAction.succ(productAction.start_tomcat(data['version']))


# 更换Jar包
@productJar_operate.route('/update', methods=['POST'])
def update_jar():
    data = json.loads(request.get_data())

    return productAction.succ(productAction.new_copy(data['version']))


# 重启产品
@productJar_operate.route('/reload_product', methods=['POST'])
def reload_product():
    data = json.loads(request.get_data())
    return productAction.succ(productAction.restart_tomcat(data['version']))


# 更换Jar包并重启产品
@productJar_operate.route('/updateReload', methods=['POST'])
def update_and_reload_product():
    data = json.loads(request.get_data())
    productAction.copy_and_reload(data['version'])
    return productAction.succ('更换jar并重启成功！')


# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
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
