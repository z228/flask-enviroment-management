from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from datetime import timedelta
from schedule import APSchedulerJobConfig
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_bootstrap import Bootstrap
from apps.lib.BaseError import *
from apps.productApp.productJar_router import *
import logging_mgr
import configs
from os.path import join
from os import getcwd, listdir

app = Flask(__name__)
app.config.from_object(configs)
db = SQLAlchemy(app)
app.debug = False
bootstrap = Bootstrap(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.from_object(APSchedulerJobConfig())
CORS(app, supports_credentials=True)
root_path = getcwd()


# 用户表
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), default="g5")
    alias = db.Column(db.String(50))
    email = db.Column(db.String(50))
    ip = db.Column(db.String(50))

    def __init__(self, username, password, alias="", email=""):
        self.username = username
        self.password = password
        self.alias = alias
        self.email = email

    def getInfo(self):
        return {"id": self.id, "username": self.username, "password": self.password, "alias": self.alias,
                "email": self.email}


# 传递图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'),
                               'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


# 主页面
@app.route('/index', methods=['POST', 'GET'])
def hello_world():
    return render_template('index.html')


def get_log_with_lines(log, lines):
    lines = lines if isinstance(lines, int) else eval(lines)
    with open(f'{app.root_path}/logs/{log}', 'r', encoding='utf-8') as logs:
        log_list = logs.readlines()
        if len(log_list) < lines:
            return ''.join(log_list)
        res_list = log_list[-1 * lines:]
        return ''.join(res_list)


@app.route('/log', methods=['POST'])
def get_log():
    req = loads(request.get_data())
    rep = {"code": 200}
    lines = req['lines']
    rep['log'] = get_log_with_lines(req['log'], lines)
    return rep


@app.route('/loglist', methods=['GET'])
def get_log_list():
    rep = {"code": 200}
    # log_list = listdir(f'{app.root_path}/logs')
    log_list = [i for i in listdir(f'{app.root_path}/logs') if '.log' in i]
    rep['logList'] = log_list
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
    db.create_all()
    app.register_blueprint(productJar_operate, url_prefix='/productJar')
    app.run(host='0.0.0.0')
