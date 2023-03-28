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





（二）设置callback

config/config.yaml

```
callback:
  callbackUrl : "http://127.0.0.1:8080/callback"
  callbackBeforeSendSingleMsg:
    enable: true 
```





（三）部署机器人
