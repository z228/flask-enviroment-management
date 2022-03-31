from time import perf_counter
from flask import Blueprint, request, render_template, send_file
from .product import ProductAction
import json
from . import test
from .status import toked
import os
from apps.lib.FtpServer import MyFTP
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'jar'}

productJar_operate = Blueprint('productJar', __name__)

# 产品jar功能页面
@productJar_operate.route('/', methods=['POST', 'GET'])
def product():
    return render_template('product.html')

# 获取脚本列表
@productJar_operate.route('/allScript', methods=['GET'])
def get_all_script():
    productAction = ProductAction()
    return productAction.succ(productAction.getAllScript())

# 执行脚本
@productJar_operate.route('/execute', methods=['post'])
def execute_script():
    data = json.loads(request.get_data())
    productAction = ProductAction()
    return productAction.succ(productAction.executeScript(data['name']))

# 删除脚本
@productJar_operate.route('/delete', methods=['post'])
def delete_script():
    data = json.loads(request.get_data())
    productAction = ProductAction()
    return productAction.succ(productAction.deleteScript(data['name']))

# 保存脚本
@productJar_operate.route('/saveScript', methods=['post'])
def save_script():
    data = json.loads(request.get_data())
    productAction = ProductAction()
    return productAction.succ(productAction.saveScript(data['content'], data['name'], data['type']))

# 获取所有版本号
@productJar_operate.route('/all', methods=['GET'])
def get_all_version():
    productAction = ProductAction()
    v = {}
    for key in productAction.config.keys():
        v[key] = productAction.config[key][0]
    return productAction.succ(v)

# 获取所有bihome
@productJar_operate.route('/allBihome', methods=['GET'])
def get_all_bihome():
    v = {}
    productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key][2].split(' ')
    return productAction.succ(v)

# 获取当前bihome
@productJar_operate.route('/currentBihome', methods=['GET'])
def get_current_bihome():
    v = {}
    productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key][3]
    return productAction.succ(v)

# 获取当前url
@productJar_operate.route('/url', methods=['GET'])
def get_url():
    v = {}
    productAction = ProductAction()
    for key in productAction.config.keys():
        if 'dis' in key:
            v[key] =productAction.config[key][1]+'/bi/?showOthers=true'
        else:
            v[key] =productAction.config[key][1]+'/bi'
    return productAction.succ(v)

# 获取141备份的jar包列表
@productJar_operate.route('/141jar', methods=['GET'])
def get_141_jar():
    v = {}
    productAction = ProductAction()
    # data = json.loads(request.get_data())
    for key in productAction.config.keys():
        key2 = "v9.4" if key == "v9.4.1"else key
        if key2 in ['v8.6','v9.0','v9.2.1','v9.4','develop']:
            v[key] = os.listdir(f'{self.ip_local}{key2}')
        else:
            v[key] = os.listdir(f'{self.ip_134}{key2}')
        v[key] = productAction.clear_list_not_num(v[key])
        v[key].sort()
        v[key].reverse()
    return productAction.succ(v)

# 更换环境bihome
@productJar_operate.route('/changeBihome', methods=['POST'])
def change_bihome():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.change_bi_home(data['version'], data['bihome']))

# 停止产品
@productJar_operate.route('/shutdown', methods=['POST'])
def shutdown_product():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    print(data['version'])
    # return succ('关闭成功')
    return productAction.succ(productAction.shut_tomcat(data['version']))

# 启动产品
@productJar_operate.route('/startup', methods=['POST'])
def start_product():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    if 'user' in data.keys():
        res = productAction.start_tomcat(data['version'],data['user'])
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
    productAction = ProductAction()
    for key in productAction.config.keys():
        if productAction.is_port_used('localhost',eval(productAction.config[key][1])):
            if  key not in toked.keys():
                v[key] =''
            else:
                v[key] =toked[key]
        else:
            v[key] ='0'
    return productAction.succ(v)

# 获取debug端口
@productJar_operate.route('/port', methods=['GET'])
def get_port():
    v = {}
    productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.get_debug_port(key)
    return productAction.succ(v)

# 获取产品端口
@productJar_operate.route('/bi', methods=['GET'])
def get_view_port():
    v = {}
    productAction = ProductAction()
    for key in productAction.config.keys():
        v[key] = productAction.config[key][1]
    return productAction.succ(v)


# 更换Jar包
@productJar_operate.route('/update', methods=['POST'])
def update_jar():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.new_copy(data['version'], data['date']))

# 更换指定日期Jar包
@productJar_operate.route('/updatewithDate', methods=['POST'])
def update_jar_with_date():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    return productAction.succ(productAction.new_copy(data['version'], data['date']))

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
    productAction = ProductAction()
    file = request.files['file']
    if 'file' not in request.files:
        return productAction.error("No file part")
    if file.filename == '':
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
        jar_path =productAction.config[version][0]+'/Yonghong/product'
        file.save(os.path.join(jar_path, filename))
        return productAction.succ(f'{file.filename} uploaded successfully')
    return productAction.error("file uploaded Fail")

# 更换Linux服务器Jar包
@productJar_operate.route('/updateLinuxJar', methods=['POST'])
def update_linux_jar():
    productAction = ProductAction()
    ftpServer = MyFTP()
    ftpServer.connect()
    ftpServer.login()
    data = json.loads(request.get_data())
    src_path = productAction.get_recent_jar(data['version'])
    dirs = os.listdir(src_path)
    for dir in dirs:
        src_file = os.path.join(src_path, dir)  
        ftpServer.upload_file(src_file, f'/{data["version"]}')
    ftpServer.quit()
    return productAction.succ(f'服务器{data["version"]}的Jar包更新成功')

# 重启产品
@productJar_operate.route('/reload_product', methods=['POST'])
def reload_product():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    if 'user' in data.keys():
        res = productAction.restart_tomcat(data['version'],data['user'])
        return productAction.succ(res)
    else:
        return productAction.succ(productAction.restart_tomcat(data['version']))

# 更换Jar包并重启产品
@productJar_operate.route('/updateReload', methods=['POST'])
def update_and_reload_product():
    productAction = ProductAction()
    data = json.loads(request.get_data())
    if 'user' in data.keys():
        res = productAction.copy_and_reload(data['version'],user=data['user'])
        return productAction.succ(res)
    else:
        return productAction.succ(productAction.copy_and_reload(data['version']))

# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
    productAction = ProductAction()
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
    productAction = ProductAction()
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
    productAction = ProductAction()
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
