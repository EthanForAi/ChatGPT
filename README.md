# chat-robot

The deployment requires Python 3.9. Run `pip3 install -r requirements.txt`.

This chatbot utilizes the callback feature of openIM. For more details about this feature, please refer to the openIM official documentation on third-party callback instructions. You need to modify the callback configuration in the openIM server, enable the "callbackBeforeSendSingleMsg" configuration. Currently, only one-on-one chat is supported.

Run the command: `python3 ./main.py --admin_id openIM123456 --api_key {{openai key}} --secret {{secret}} --im_api_url http://127.0.0.1:10002 --rebot_user_id {{your rebot id}} --host 127.0.0.1 --port 8080 --redis_addr 127.0.0.1:16379 --redis_pwd openIM123`

The `admin_id` is the openIM admin's ID, `api_key` is the ChatGPT API key, `secret` is your openIM system's secret, `im_api_url` is the IM API address, `rebot_user_id` is the user ID you want to act as a chatbot. When you send a question to this user, the chatbot will call ChatGPT and reply to you. `host` is the callback server listening address, `port` is the callback server's port, which by default is consistent with the openIM configuration. `redis_addr` and `redis_pwd` are the Redis address and password, by default consistent with the openIM's default configuration.





部署版本需要python3.9 pip3 install -r requirements.txt 该机器人使用了openIM的回调功能，关于该功能具体查看openIM官网的第三方回调说明文档。 需要修改openIM服务端的callback配置，打开callbackBeforeSendSingleMsg配置，将他的enable设置为true。

 运行命令 python3 ./main.py --admin_id openIM123456 --api_key {{openai key}} --secret {{secret}} --im_api_url http://127.0.0.1:10002 --rebot_user_id {{your rebot id}} --host 127.0.0.1 --port 8080 --redis_addr 127.0.0.1:16379 --redis_pwd openIM123 admin_id为openIM管理员的id, api_key为 chatgpt的密钥 secret为你openIM系统的密钥 im_api_url为im的api地址 rebot_user_id为你想要当作机器人的用户ID 向该用户发送问题，该用户调用chatgpt然后回复你。 host为回调服务器监听地址，port为该callback服务器的端口，默认和openIM配置文件保持一致。redis_addr和redis_pwd为redis的地址和密码，默认和openIM的默认配置保持一致。 

