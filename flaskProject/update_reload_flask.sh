#!/bin/bash
res=`lsof -i:5000`
#port=`lsof -i:5000 | awk '{print $2}' | grep "[0-9]"`
cmd=`lsof -i:5000 | awk '{print $1}' | grep "[^COMMAND]"`
echo "$res"
# echo "kill -9 $port"
echo "$cmd"
if [ "$cmd" = "python3" ]; then
    cd /opt/my-first-flask/flaskProject
    echo "更新本地代码"
    git pull
    echo "关闭flask"
    lsof -i:5000 | awk '{print $2}' | grep "[0-9]" | xargs kill -9
    echo "后台运行flask"
    nohup python3 -u app.py >run.log 2>&1 &
else
    echo "flask没有在运行"
    echo "更新本地代码"
    git pull
    echo "后台运行flask"
    nohup python3 -u app.py >run.log 2>&1 &
fi
#kill -9 port
