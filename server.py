from aiohttp import web
import asyncio
import logging

import config

app = web.Application()
queue = asyncio.Queue()

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
        if recv_id == config.rebot_user_id and content_type==101 and send_id != config.rebot_user_id:
            print("operationID is {}, recvID is {}".format(operation_id, recv_id))
            await queue.put(body)
        return web.json_response(resp)

app.router.add_view("/callback", Server)

def start_server(host, port):
    logging.info("start server host is {}, port is {}".format(host, port))
    web_server = web._run_app(app, host=host, port=port)
    return web_server

