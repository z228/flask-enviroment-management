from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from venu import watermark, OCR, hua, copy, restart
from datetime import timedelta
from config import APSchedulerJobConfig
from flask_apscheduler import APScheduler

# clean.static_clean() #清理资源文件夹
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(APSchedulerJobConfig())
scheduler = APScheduler()  # 实例化APScheduler
scheduler.init_app(app)  # 把任务列表载入实例flask
scheduler.start()  # 启动任务计划


# 主页面
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        return redirect(url_for('choose'))
    return render_template('index.html')


# 去水印图片上传页面
@app.route('/watermark_upload', methods=['POST', 'GET'])
def watermark_upload():
    if request.method == 'POST':
        f = request.files['file']
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(base_path, 'static/uploads',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        res = watermark.mark(f.filename)
        return redirect(url_for('watermark_after_upload', name=res))
    return render_template('watermark_upload.html')


# 选择功能页面
@app.route('/choose', methods=['POST', 'GET'])
def choose():
    if request.method == 'POST':
        if request.form.get('string'):
            return redirect(url_for('upload'))
        elif request.form.get('water'):
            return redirect(url_for('watermark_upload'))
    return render_template('choose.html')


# 图片上传
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        txt = request.form.get('txt')
        if txt == '':
            return '''<h1 >请输入填充字符!</h1> 
            <script type="text/javascript">setTimeout("history.go(-1)", 3000);  </script>
            <SCRIPT language=javascript>
            function go()
            {
             window.history.go(-1);
            }
            setTimeout("go()",3000);
            </SCRIPT>
            '''
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(base_path, 'static/uploads',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

        # f.save(upload_path)
        f1 = hua.change(txt, f)
        return redirect(url_for('after_upload', name=f1))
    return render_template('upload.html')


@app.route('/after_upload/<name>', methods=['POST', 'GET'])
def after_upload(name=None):
    if request.method == 'POST':
        return send_from_directory('./static/result', name, as_attachment=True)
    return render_template('after_upload.html', name=name)


@app.route('/watermark_after_upload/<name>', methods=['POST', 'GET'])
def watermark_after_upload(name=None):
    if request.method == 'POST':
        if request.form.get('water'):
            res = watermark.mark(name)
            return redirect(url_for('watermark_after_upload', name=res))
        elif request.form.get('sharpen'):
            #  res = sharpen.sharpen(name)
            return redirect(url_for('watermark_upload'))
        elif request.form.get('OCR'):
            txt = OCR.ocr(name)
            return txt
        else:
            return send_from_directory('./static/result', name, as_attachment=True)
    return render_template('watermark_after_upload.html', name=name)


# 产品jar功能页面
@app.route('/product', methods=['POST', 'GET'])
def product():
    if request.method == 'POST':
        if request.form.get('exchange'):
            return redirect(url_for('exchange'))
        elif request.form.get('reload'):
            return redirect(url_for('reload'))
    return render_template('product.html')


# 更换jar功能页面
@app.route('/exchange', methods=['POST', 'GET'])
def exchange():
    if request.method == 'POST':
        aim = request.form['exchange']
        print(request.form['exchange'])
        log = copy.new_copy(aim)
        return log + '''<script type="text/javascript">setTimeout("history.go(-1)", 10000);  </script>
                    <SCRIPT language=javascript>
                    function go()
                    {
                     window.history.go(-1);
                    }
                    setTimeout("go()",3000);
                    </SCRIPT>
                    '''
        # request.form.
    return render_template('exchange.html')


# 重启服务功能页面
@app.route('/reload', methods=['POST', 'GET'])
def reload():
    if request.method == 'POST':
        aim = request.form['reload']
        print(request.form['reload'])
        log = restart.restart_tomcat(aim)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
