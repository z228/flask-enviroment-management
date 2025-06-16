# 定时任务
class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'clean_jar',  # 任务唯一ID
            'func': 'apps.productApp.task:clean_jar',
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 1,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'shutdown_trunk_tomcat',  # 任务唯一ID
            'func': 'apps.productApp.task:shutdown_trunk_tomcat',
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 20,
            'minute': 0,
            'second': 0
        },
        {
            'id': 'upload_jacoco_file',  # 任务唯一ID
            'func': 'apps.productApp.task:upload_jacoco_file',
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 20,
            'minute': 30,
            'second': 0
        },
        {
            'id': 'commit_junit_exp',  # 任务唯一ID
            'func': 'apps.productApp.task:commit_junit_exp',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
            # 'trigger': 'interval',
            # 'seconds': 60 * 60 * 1
        },
        {
            'id': 'getResJunit',  # 任务唯一ID
            'func': 'apps.productApp.getResJunit:main',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'xls_diff_res',  # 任务唯一ID
            'func': 'apps.productApp.jobs.genReport.genJunitHtml:seq_exec_job',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'cleanResPng',  # 任务唯一ID
            'func': 'apps.productApp.jobs.genReport.genJunitHtml:clean_yesterday_res',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': [2],  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'genDiffImg',  # 任务唯一ID
            'func': 'apps.productApp.jobs.genReport.genJunitHtml:generate_diff_img',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': [2],  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'genReport',  # 任务唯一ID
            'func': 'apps.productApp.jobs.genReport.genJunitHtml:generate_report',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': [2],  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'juejin_checkIn',  # 任务唯一ID
            'func': 'apps.productApp.task:juejin_checkin',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 6,
            'minute': 30,
            'second': 0
        },
        {
            'id': 'clean_memory_cache',  # 任务唯一ID
            'func': 'apps.productApp.task:clean_memory_cache',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            # 'trigger': 'date',
            # 'run_date': '2099-8-30 01:00:00'
            'trigger': 'interval',
            'seconds': 60 * 20
        },
        {
            'id': 'test_job',  # 任务唯一ID
            'func': 'apps.productApp.task:test_job',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': [2],  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
        },
        {
            'id': 'update_v2ray_geo',  # 任务唯一ID
            'func': 'apps.productApp.task:update_v2ray_geo',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'date',
            'run_date': '2099-8-30 01:00:00'
            # 'trigger': 'cron',
            # 'hour': 4,
            # 'minute': 30,
            # 'second': 0
        },
        {
            'id': 'every_day_list',  # 任务唯一ID
            'func': 'apps.productApp.task:every_day_list',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 2,
            'minute': 30,
            'second': 0
        }
        ,
        {
            'id': 'kill_all_pptr',  # 杀死所有node_pptr进程
            'func': 'apps.productApp.task:kill_all_pptr',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': None,  # 如果function需要参数，就在这里添加
            'replace_existing': True,
            'trigger': 'cron',
            'hour': 2,
            'minute': 15,
            'second': 0
        }
    ]
