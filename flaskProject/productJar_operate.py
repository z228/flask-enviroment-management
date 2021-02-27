from flask import Blueprint, request, redirect, render_template, url_for
from product import *

productJar_operate = Blueprint('productJar', __name__)


# 产品jar功能页面
@productJar_operate.route('', methods=['POST', 'GET'])
def product():
    if request.method == 'POST':
        if request.form.get('exchange'):
            return redirect(url_for('productJar.exchange'))
        elif request.form.get('reload'):
            return redirect(url_for('productJar.reload'))
    return render_template('product.html')


# 更换jar功能页面
@productJar_operate.route('/exchange', methods=['POST', 'GET'])
def exchange():
    if request.method == 'POST':
        aim = request.form['exchange']
        print(request.form['exchange'])
        log = new_copy(aim)
        return '''<link rel="shortcut icon" href="{{ url_for('productJar.static', 
        filename='favicon.ico') }}">''' + log
        # request.form.
    return render_template('exchange.html')


# 重启服务功能页面
@productJar_operate.route('/reload', methods=['POST', 'GET'])
def reload():
    if request.method == 'POST':
        aim = request.form['reload']
        print(request.form['reload'])
        log = restart_tomcat(aim)
        return log + '''<script type="text/javascript">setTimeout("history.go(-1)", 10000);  </script>
                            <SCRIPT language=javascript>
                            function go()
                            {
                             window.history.go(-1);
                            }
                            setTimeout("go()",3000);
                            </SCRIPT>
                            '''
    return render_template('reload.html')
