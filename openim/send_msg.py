from hashlib import md5
from random import random
from secrets import choice
import string
import requests
import json
import aiohttp

import config
import utils

class Open_im_api:
    def __init__(self, secret, admin_id, base_url) -> None:
        self.secret = secret
        self.admin_id = admin_id
        self.base_url = base_url
        self.token = ""

    async def request(self, route, data):
        headers = {"token": self.token}
        resp = await self.make_post_request(self.base_url+route, data=data, headers=headers)
        print(resp)
        if resp.get("errCode") != 0:
            raise Exception("errCode is {}, errMsg is{}".format(resp.get("errCode"), resp.get("errMsg")))
        return resp

    async def make_post_request(self, url, data, headers):
        async with aiohttp.ClientSession() as session:
            data = json.dumps(data)
            async with session.post(url, data=data, headers=headers) as response:
                return await response.json()

    async def get_admin_token(self, admin_id) -> string: 
        data = {
            "secret": config.secret,
            "platform": 1,
            "userID": admin_id,
            "operationID": "rebot get token"
        }
        resp = await self.request("/auth/user_token", data=data)
        return resp["data"]["token"]

    @utils.async_retry(num_retries=3, delay=0.1)
    async def send_msg(self, recv_id, content):
        msg = {
            "operationID": "chatgptoperationid", 
            "sendID": config.rebot_user_id, 
            "recvID": recv_id,
            "senderPlatformID": 1, 
            "content": {
                "text": content
            },
            "contentType": 101, 
            "sessionType": 1, 
            "isOnlineOnly": False
        }
        print(msg)
        await self.request("/msg/manage_send_msg", msg)