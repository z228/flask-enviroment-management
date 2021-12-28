import os

from flask import Blueprint, request, redirect, render_template, url_for, send_from_directory

from Image_feature import mark, change, ocr

image_operate = Blueprint('image', __name__)


# 去水印图片上传页面
@image_operate.route('/watermark_upload', methods=['POST', 'GET'])
def watermark_upload():
    if request.method == 'POST':

        f = request.files['file']
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = base_path + './static/uploads/' + f.filename
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        if request.form.get('water'):
            res = mark(f.filename)
            return redirect(url_for('image.watermark_after_upload', name=res))
        elif request.form.get('sharpen'):
            #  res = sharpen.sharpen(name)
            return redirect(url_for('image.watermark_upload'))
        elif request.form.get('ocr'):
            txt = ocr(f.filename)
            return txt
    return render_template('watermark_upload.html')


# 选择功能页面
@image_operate.route('/choose', methods=['POST', 'GET'])
def choose():
    if request.method == 'POST':
        if request.form.get('string'):
            return redirect(url_for('image.upload'))
        elif request.form.get('water'):
            return redirect(url_for('image.watermark_upload'))
    return render_template('choose.html')


# 图片上传
@image_operate.route('/upload', methods=['POST', 'GET'])
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
        upload_path = base_path + './static/uploads/' + f.filename
        # f.save(upload_path)
        f1 = change(txt, f)
        return redirect(url_for('image.after_upload', name=f1))
    return render_template('upload.html')


@image_operate.route('/after_upload/<name>', methods=['POST', 'GET'])
def after_upload(name=None):
    if request.method == 'POST':
        return send_from_directory('./static/results', name, as_attachment=True)
    return render_template('after_upload.html', name=name)


@image_operate.route('/watermark_after_upload/<name>', methods=['POST', 'GET'])
def watermark_after_upload(name=None):
    if request.method == 'POST':
        if request.form.get('water'):
            res = mark(name)
            return redirect(url_for('image.watermark_after_upload', name=res))
        elif request.form.get('sharpen'):
            #  res = sharpen.sharpen(name)
            return redirect(url_for('image.watermark_upload'))
        elif request.form.get('OCR'):
            txt = ocr(name)
            return txt
        else:
            return send_from_directory('./static/results', name, as_attachment=True)
    return render_template('watermark_after_upload.html', name=name)
