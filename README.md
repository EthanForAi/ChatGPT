# ChatGPT
扫码进群交流
![](https://github.com/EthanForAi/ChatGPT/blob/main/img/wechat.jpg)
## 功能介绍

由于ChatGPT只提供了单纯的api，提供完整服务需要额外的开发工作。OpenIM把实时推送、消息记录、会话隔离、上下文管理、多端同步等强大的工程能力赋予了ChatGPT，协助开发者打造真正的聊天机器人

## 部署OpenIM

1. 使用该机器人需要先部署openIM服务器 [open-im-server部署文档](https://doc.rentsoft.cn/#/v2/validation/all)

   1. 1项目clone

   ```
   git clone https://github.com/OpenIMSDK/Open-IM-Server.git --recursive;Copy to clipboardErrorCopied
   ```

   1. 2初始化安装

   ```
   cd  Open-IM-Server; chmod +x install_im_server.sh; ./install_im_server.sh;Copy to clipboardErrorCopied
   ```

   1. 3检查服务

   ```
   cd script;./docker_check_service.sh
   ```

   ![](https://github.com/EthanForAi/ChatGPT/blob/main/docs/docker_success.png)

2. 设置callback
   该机器人使用了openIM的回调功能，关于该功能具体查看openIM官网的第三方回调说明文档。[第三方回调官方文档](https://doc.rentsoft.cn/#/callback/callback)

   config/config.yaml

```
callback:
  callbackUrl : "http://127.0.0.1:8080/callback"
  callbackBeforeSendSingleMsg:
    enable: true 
  callbackBeforeSendGroupMsg:
    enable: true
```

3. 重启

```
docker-compose down; docker-compose up -d
```

## 部署callback打通OpenIM和ChatGPT

### docker部署(推荐)

最新镜像：openim/chat_gpt:v0.0.1

```
 docker run --name open_im_chat_gpt --net=host openim/chat_gpt:v0.0.1 python3 main.py --admin_id openIM123456 --api_key {{openai key}} --secret {{secret}} --im_api_url http://127.0.0.1:10002 --robot_user_id {{your robot id}} --host 127.0.0.1 --port 8080 --redis_addr 127.0.0.1:16379 --redis_pwd openIM123
```

###  源码部署

部署版本需要python3.9（需要安装好python包管理工具pip3）

安装命令： pip3 install -r requirements.txt

运行命令

```
 python3 ./main.py --admin_id openIM123456 --api_key {{openai key}} --secret {{secret}} --im_api_url http://127.0.0.1:10002 --robot_user_id {{your robot id}} --host 127.0.0.1 --port 8080 --redis_addr 127.0.0.1:16379 --redis_pwd openIM123
```

### 启动参数详解

| 参数          | 详解                                                         |
| ------------- | ------------------------------------------------------------ |
| admin_id      | openIM管理员的userID, config.yaml文件manager.appManagerUid中的一个，默认为openIM123456 |
| api_key       | openai的密钥，自行获取                                       |
| secret        | openIM系统的密钥secret，.env中的PASSWORD，默认为openIM123    |
| im_api_url    | im消息推送api，如果单机部署则默认为http://127.0.0.1:10002    |
| robot_user_id | 机器人userID，需先手动注册，英文字母和数字组成，注意不能和其他userID重复。 |
| host          | im消息callback ip(单机部署默认为127.0.0.1，和openIM config.yaml的callback配置一样) |
| port          | im消息callback 端口(默认8080，和openIM config.yaml的callback配置一样) |
| redis_addr    | 保存会话上下文使用redis，redis的地址， 单机部署默认为127.0.0.1:16379 |
| redis_pwd     | redis_pwd 密码， 单机部署默认为openIM123                     |


## 部署验证和效果演示

部署成功验证![avatar](https://github.com/EthanForAi/ChatGPT/blob/main/img/deploy.png)

单聊效果演示![avatar](https://github.com/EthanForAi/ChatGPT/blob/main/img/single.jpg)


群聊效果演示![avatar](https://github.com/EthanForAi/ChatGPT/blob/main/img/group.jpg)

