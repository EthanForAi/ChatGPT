import asyncio

import server

from openim import Open_im_api
import config
import rebot
import traceback

import cache

async def start_consumer():
    consumer = Consumer()
    await consumer.init_open_im_api()
    await consumer.run()

class Consumer:
    def __init__(self):
        self.open_im_api = Open_im_api(secret=config.secret, admin_id=config.admin_id, base_url=config.im_api_url)
        self.chat_gpt = rebot.Chat_gpt()

    async def init_open_im_api(self):
        token = await self.open_im_api.get_admin_token(config.admin_id)
        self.open_im_api.token = token
        print("token is {}".format(token))

    async def run(self):
        while True:
            msg = await server.queue.get()
            task = asyncio.create_task(self.consume_chat_gpt(msg))
            await task
    
    # recvID is gpt
    async def consume_chat_gpt(self, msg):
        content = msg.get("content")
        recv_id = msg.get("recvID")
        send_id = msg.get("sendID")
        print(content, recv_id, send_id)
        try:    
            gpt_resp = ""
            historys = await cache.redis_client.client.lrange(cache.redis_client.get_key(send_id), 0, -1)
            # 新会话
            if len(historys) == 0:
                print(send_id, "new conversation")
                gpt_resp = await self.chat_gpt.ask_chat_gpt(content)
            else:
                s1 = list()
                for i in historys:
                    s1.append(i.decode("utf-8"))
                gpt_resp = await self.chat_gpt.ask_chat_gpt_context(content, s1)
           
            await cache.redis_client.client.lpush(cache.redis_client.get_key(send_id), content, gpt_resp)
            await cache.redis_client.client.expire(cache.redis_client.get_key(send_id), 200)
            await self.open_im_api.send_msg(recv_id=send_id, content=gpt_resp)
            print("reply ok!!!")
        except Exception as e:
            print(e)
            traceback.print_exc(e)

