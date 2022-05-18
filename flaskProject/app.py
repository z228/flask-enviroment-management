from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from datetime import timedelta
from config import APSchedulerJobConfig
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_bootstrap import Bootstrap
from apps.lib.BaseError import *
from apps.productApp.productJar_router import *
import logging_mgr
from os.path import join


# clean.static_clean() #清理资源文件夹
app = Flask(__name__)
app.register_blueprint(productJar_operate, url_prefix='/productJar')
app.debug = True
bootstrap = Bootstrap(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(APSchedulerJobConfig())
CORS(app, supports_credentials=True)


# 传递图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'),
                               'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


# 主页面
@app.route('/index', methods=['POST', 'GET'])
def hello_world():
    return render_template('index.html')

def get_log_with_lines(module, lines):
    res = ''
    lines = lines if isinstance(lines, int) else  eval(lines)
    with open(f'./logs/{module}.log', 'r', encoding='utf-8') as logs:
        log_list = logs.readlines()
        if len(log_list) < lines:
            return ''.join(log_list)
        log_list.reverse()
        res_list = log_list[0:lines]
        res_list.reverse()
        return ''.join(res_list)


@app.route('/flasklog', methods=['POST'])
def get_flask_log():
    req = loads(request.get_data())
    rep = {"code": 200}
    lines = req['lines']
    rep['log'] = get_log_with_lines('flask',lines)
    return rep


@app.route('/debuglog', methods=['POST'])
def get_debug_log():
    req = loads(request.get_data())
    rep = {"code": 200}
    lines = req['lines']
    rep['log'] = get_log_with_lines('debug',lines)
    return rep


@app.route('/tasklog', methods=['POST'])
def get_task_log():
    req = loads(request.get_data())
    rep = {"code": 200}
    lines = req['lines']
    rep['log'] = get_log_with_lines('task',lines)
    return rep


@app.errorhandler(BaseError)
def custom_error_handler(e):
    if e.level in [BaseError.LEVEL_WARN, BaseError.LEVEL_ERROR]:
        if isinstance(e, OrmError):
            app.logger.exception('%s %s' % (e.parent_error, e))
        else:
            app.logger.exception('错误信息: %s %s' % (e.extras, e))
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


if __name__ == '__main__':
    # os.symlink(log_path, log_path_today)
    scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表载入实例flask
    scheduler.start()  # 启动任务计划
    app.run(host='0.0.0.0')
