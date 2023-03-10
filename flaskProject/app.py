from flask import Flask, send_from_directory,jsonify
from flask_cors import CORS
import os
from datetime import timedelta
from config import APSchedulerJobConfig
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import TimedRotatingFileHandler
from apps.lib.BaseError import *
from apps.productApp.productJar_router import *
from apps.lib.MyHandlers import *

# clean.static_clean() #清理资源文件夹
app = Flask(__name__)
app.register_blueprint(productJar_operate, url_prefix='/productJar')
app.debug = True
bootstrap = Bootstrap(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(APSchedulerJobConfig())
CORS(app, supports_credentials=True)
scheduler = APScheduler()  # 实例化APScheduler
scheduler.init_app(app)  # 把任务列表载入实例flask
scheduler.start()  # 启动任务计划


# 传递图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


# 主页面
@app.route('/index', methods=['POST', 'GET'])
def hello_world():
    return render_template('index.html')

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
    log_path = './logs/flask.log'
    log_path_today = f'./logs/flask.log'
    handler = MidnightRotatingFileHandler(log_path)   # 设置日志字符集和存储路径名字
    logging_format = logging.Formatter(                            # 设置日志格式
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    # os.symlink(log_path, log_path_today)
    app.run(host='0.0.0.0')
