# MyFirstFlask

#### 介绍


#### 软件架构
##### 前端
vue
##### 后端
python(3.6)+flask

#### 使用说明

1.  后端可以直接`python app.py`运行
2.  前端目录先运行`npm install`,在调试时直接运行`npm run serve`
3.  前端部署到nginx上时步骤：
    + 前端根目录下运行`npm run build`
    + 在nginx中 nginx.conf 添加对应的serve配置配置如下：
    ```
    server {
        listen       9999;
        server_name  localhost;
        location / {
            root   /opt/html;
            try_files $uri $uri/ /index.html last;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    ```
    + `/opt/html`可以自己修改为前端build出来的dist目录
    + nginx的重启命令：`nginx -s reload`，Windows上自行重启服务即可
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
