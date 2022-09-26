# 定时任务
class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        # {
        #     'id': 'No1',  # 任务唯一ID
        #     'func': 'task:static_clean',
        #     # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
        #     'args': None,  # 如果function需要参数，就在这里添加
        #     'trigger': 'cron',
        #     'hour': 0,
        #     'minute': 0,
        #     'second': 0
        # },
        {
            'id': 'No2',  # 任务唯一ID
            'func': 'apps.productApp.task:killall_java',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 23,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'No4',  # 任务唯一ID
            'func': 'apps.productApp.task:copy_jar_to_local',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'interval',
            'seconds': 300
        },
        {
            'id': 'No5',  # 任务唯一ID
            'func': 'apps.productApp.task:clean_backup_jar',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 0,
            'minute': 30,
            'second': 0
        },
        {
            'id': 'No6',  # 任务唯一ID
            'func': 'apps.productApp.task:copy_jacoco_to_192',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'cron',
            'hour': 23,
            'minute': 10,
            'second': 0
        },
        {
            'id': 'No6',  # 任务唯一ID
            'func': 'apps.productApp.task:get_jar_list',
            'args': None,  # 如果function需要参数，就在这里添加
            'trigger': 'interval',
            'seconds': 50
        }
    ]
