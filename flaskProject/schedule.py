# 定时任务
class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'clean_jar',  # 任务唯一ID
            'func': 'apps.productApp.task:clean_jar',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 1,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'shutdown_trunk_tomcat',  # 任务唯一ID
            'func': 'apps.productApp.task:shutdown_trunk_tomcat',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 23,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'upload_jacoco_file',  # 任务唯一ID
            'func': 'apps.productApp.task:upload_jacoco_file',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 23,
            'minute': 30,
            'second': 0
        },
        {
            'id': 'commit_junit_exp',  # 任务唯一ID
            'func': 'apps.productApp.task:commit_junit_exp',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'interval',
            'seconds': 60 * 60 * 2
        },
        {
            'id': 'getResJunit',  # 任务唯一ID
            'func': 'apps.productApp.getResJunit:main',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 8,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'juejin_checkIn',  # 任务唯一ID
            'func': 'apps.productApp.task:juejin_checkin',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 6,
            'minute': 30,
            'second': 0
        }
    ]
