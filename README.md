（一）部署OpenIM

```
git clone https://github.com/OpenIMSDK/Open-IM-Server.git --recursive;
```

```
cd  Open-IM-Server; chmod +x install_im_server.sh; ./install_im_server.sh;
```

```
cd script;./docker_check_service.sh
```

```
```

![](https://github.com/EthanForAi/ChatGPT/blob/main/docs/docker_success.png)



（二）设置callback

config/config.yaml

```
callback:
  callbackUrl : "http://127.0.0.1:8080/callback"
  callbackBeforeSendSingleMsg:
    enable: true 
  callbackBeforeSendGroupMsg:
    enable: true
```





## 部署chatGPT机器人

### docker部署(推荐)
最新镜像：openim/chat_gpt:v0.0.1
```
 docker run --name open_im_chat_gpt --net=host openim/chat_gpt:v0.0.1 python3 main.py --admin_id openIM123456 --api_key {{openai key}} --secret {{secret}} --im_api_url http://127.0.0.1:10002 --robot_user_id {{your robot id}} --host 127.0.0.1 --port 8080 --redis_addr 127.0.0.1:16379 --redis_pwd openIM123
```

###  源码部署
部署版本需要python3.9（需要安装好python包管理工具pip3）

安装命令： pip3 install -r requirements.txt