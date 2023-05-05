import asyncio
import argparse
import sys
import openai

# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from server import start_server
import config
import consumer
import cache
import log

def parse_arguments(argv):
    parser = argparse.ArgumentParser() 
    parser.add_argument('--admin_id', type=str, default=config.admin_id, help='openIM adminID')
    parser.add_argument('--api_key', type=str, default=config.api_key, help="chatgpt's apiKey")
    parser.add_argument('--secret', type=str, default=config.secret, help='openIM secret')
    parser.add_argument('--im_api_url', type=str, default=config.im_api_url, help='openIM api url')
    parser.add_argument('--robot_user_id',type=str, default=config.robot_user_id, help='robot userID in openIM')
    parser.add_argument("--redis_addr", type=str, default=config.host, help="redis addr")
    parser.add_argument("--redis_pwd", type=str, default=config.host, help="redis pwd")
    parser.add_argument('--host', type=str, default =config.host, help='robot server listen host')
    parser.add_argument('--port', type=int, default =config.port, help='robot server listen port')
    args = parser.parse_args(argv)
    if args.admin_id:
        config.admin_id = args.admin_id
    if args.api_key:
        config.api_key = args.api_key
    if args.secret:
        config.secret = args.secret
    if args.im_api_url:
        config.im_api_url = args.im_api_url
    if args.robot_user_id:
        config.robot_user_id = args.robot_user_id
    if args.redis_addr:    
        config.redis_addr = args.redis_addr
    if args.redis_pwd:
        config.redis_pwd = args.redis_pwd
    if args.host:    
        config.host = args.host
    if args.port:    
        config.port = args.port
    if args.api_key:
        config.api_key = args.api_key    
    openai.api_key = config.api_key
    openai.api_base = "https://api.openai.com/v2"
    # openai.
    return args    
  
async def main():
    args = parse_arguments(sys.argv[1:])
    await cache.redis_client.init_redis(args.redis_addr, args.redis_pwd)
    asyncio.create_task(start_server(config.host, config.port))
    asyncio.create_task(consumer.start_consumer())

if __name__ == "__main__":
    log.info("","start robot callback server")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()