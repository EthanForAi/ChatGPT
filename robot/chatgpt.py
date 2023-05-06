import openai

from robot import robot
import utils

import json
import log

engine = "gpt-3.5-turbo"
davinci_engine = "text-davinci-003"

class Chat_gpt(robot):
    def __init__(self) -> None:
        super().__init__()
        self.request_timeout = 60
        self.prompt_a = str()
        self.prompt_b = str()
        self.__init_prompt("./")

    def __init_prompt(self, path):
        with open(path+"prompt_a.json", "r", encoding="utf-8") as f:
            s = f.read()
            self.prompt_a = json.loads(s)

        with open(path+"prompt_b.json", "r", encoding="utf-8") as f2:
            s = f2.read()
            self.prompt_b = json.loads(s)

        log.info("", self.prompt_b)
        log.info("", self.prompt_b)

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt(self, question):
        messages = [self.prompt_b, {"role":"user", "content": question}]
        completions = await openai.ChatCompletion.acreate(
            model=engine,
            messages=messages,
            request_timeout=self.request_timeout
        )
        return completions['choices'][0]['message']['content'].strip()

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt_context(self, question, args):
        args.reverse()
        args.append(question)
        prompt = '\n'.join(args)[-1000:]
        # completions = await openai.ChatCompletion.acreate(
        #     model=engine,
        #     prompt=prompt,
        #     max_tokens=2500,
        #     n=1,
        #     temperature=0.5,
        #     request_timeout=self.request_timeout,
        # )
        messages = [self.prompt_b, {"role":"user", "content": prompt}]
        completions = await openai.ChatCompletion.acreate(
            model=engine,
            messages=messages,
            request_timeout=self.request_timeout,
        )
        return completions['choices'][0]['message']['content'].strip()
