import asyncio
import re
import server

from openim import Open_im_api
import config
import robot
import json
import traceback

import cache

import log

async def start_consumer():
    consumer = Consumer()
    await consumer.init_open_im_api()
    asyncio.create_task(consumer.run_group())
    asyncio.create_task(consumer.run_single())

class Consumer:
    def __init__(self):
        self.open_im_api = Open_im_api(secret=config.secret, admin_id=config.admin_id, base_url=config.im_api_url)
        self.chat_gpt = robot.Chat_gpt()

    async def init_open_im_api(self):
        token = await self.open_im_api.get_admin_token(config.admin_id)
        self.open_im_api.token = token
        log.info("","token is {}".format(token))

    async def run_single(self):
        while True:
            msg = await server.single_chat_queue.get()
            asyncio.create_task(self.consume_single_chat(msg))
        
    async def run_group(self):
         while True:
            msg = await server.group_chat_queue.get()
            asyncio.create_task(self.consume_group_chat(msg))

    async def handle_msg(self, key, content):
        historys = await cache.redis_client.client.lrange(key, 0, 4)
        # 新会话
        if len(historys) == 0:
            gpt_resp = await self.chat_gpt.ask_chat_gpt(content)
        else:
            s = list()
            for i in historys:
                s.append(i.decode("utf-8"))
            gpt_resp = await self.chat_gpt.ask_chat_gpt_context(content, s)
        if len(gpt_resp) > 0:
            if gpt_resp[0] == "?" or gpt_resp[0] == "？":
                gpt_resp = gpt_resp[1:]
        gpt_resp = gpt_resp.strip()        
        await cache.redis_client.client.lpush(key, content, gpt_resp)
        await cache.redis_client.client.expire(key, 60*60*24)
        return gpt_resp
    
    # single
    async def single(self, operation_id, user_id, content):
        gpt_resp = await self.handle_msg(cache.redis_client.get_key(user_id), content)
        log.info(operation_id, "gpt resp success")
        await self.open_im_api.send_msg(recv_id=user_id, text=gpt_resp)

    # group
    async def group(self, operation_id, user_id, group_id, content, session_type, sender_nickname):
        gpt_resp = await self.handle_msg(cache.redis_client.get_group_key(user_id, group_id), content)
        log.info(operation_id, "gpt resp success")
        await self.open_im_api.send_at_msg(group_id=group_id, text=gpt_resp, at_user_id=user_id, session_type=session_type, sender_nickname=sender_nickname)


    # recvID is gpt
    async def consume_single_chat(self, msg):
        content = msg.get("content")
        send_id = msg.get("sendID")
        operation_id = msg.get("operationID")
        try:    
           await self.single(operation_id, send_id, content)
        except Exception as e:
            log.error(operation_id, "single chatgpt failed {}".format(e))
            traceback.print_exc()
            try:
                await self.open_im_api.send_msg(recv_id=send_id, text=str(e))
            except Exception as e2:
                log.error(operation_id, "send error msg failed "+e2)

    async def consume_group_chat(self, msg):
        content = msg.get("content")
        text = ""
        if content:
            content = json.loads(content)
            text = content.get("text")
            reg = re.compile(r'@\S+\s?')
            text = reg.sub("", text)

        group_id = msg.get("groupID")
        session_type = msg.get("sessionType")
        send_id = msg.get("sendID")
        operation_id = msg.get("operationID")
        sender_nickname = msg.get("senderNickname")
        if text == "":
            return
        for i in text:
            if i != " ":
                break
        else:
            return
    
        try:    
           await self.group(operation_id, send_id, group_id, text, session_type, sender_nickname)
        except Exception as e:
             traceback.print_exc()
            log.error(operation_id, "chatgpt in group error {}".format(e))
            try:
                await self.open_im_api.send_at_msg(group_id=group_id, text=str(e), at_user_id=send_id, session_type=session_type, sender_nickname=sender_nickname)
            except Exception as e2:
                log.error(operation_id, "send error msg failed, error {}".format(e2))
