from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

HOST = 'localhost'
PORT = '3306'
DATABASE = 'flask1'
USERNAME = 'root'
PASSWORD = '9926'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD, host=HOST,
                                                                                        port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
SCHEDULER_API_ENABLED = True  # 调度器开关

# 配置mysql
SQLALCHEMY_DATABASE_URI = DB_URI
# job存储位置
SCHEDULER_JOBSTORES = {
    'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
}
# 线程池配置
SCHEDULER_EXECUTORS = {
    'default': {'type': 'threadpool', 'max_workers': 10}
}
