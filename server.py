from aiohttp import web
import asyncio
import json

import log
import config


app = web.Application()
single_chat_queue = asyncio.Queue()
group_chat_queue = asyncio.Queue()

resp = {
        "actionCode": 0,
        "errCode": 0,
        "errMsg": "",
        "operationID": "",
        }

class Server(web.View):
    async def post(self):
        body = await self.request.json()
        body = dict(body)
        operation_id = body.get("operationID")
        recv_id = body.get("recvID")
        send_id = body.get("sendID")
        content_type = body.get("contentType")
        callback_command = body.get("callbackCommand")

        group_id = body.get("groupID")
        log.info(operation_id, body)
        if (callback_command=="callbackBeforeSendSingleMsgCommand" or callback_command == "callbackBeforeSendGroupMsgCommand") and send_id != config.robot_user_id:
            
            if group_id and content_type == 106:
                content = body.get("content")
                at_content = json.loads(content)
                at_user_list = at_content.get("atUserList")
                if config.robot_user_id in at_user_list:
                    log.info(operation_id, "recv group msg")
                    await group_chat_queue.put(body)  
            if recv_id == config.robot_user_id and content_type == 101:
                log.info(operation_id, "recv single msg")
                await single_chat_queue.put(body)
        return web.json_response(resp)

app.router.add_view("/callback", Server)

def start_server(host, port):
    web_server = web._run_app(app, host=host, port=port)
    return web_server

