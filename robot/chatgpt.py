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
        self.prompt = dict()
        self.__init_prompt("./prompt.json")

    def __init_prompt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
            self.prompt = json.loads(s)
        log.info("", "init prompt success", self.prompt)

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt(self, question):
        completions = await openai.ChatCompletion.acreate(
            model=engine,
            messages=self.prompt
        )
        return completions.choices[0].text

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt_context(self, question, args):
        args.reverse()
        args.append(question)
        prompt = '\n'.join(args)[-1000:]
        completions = await openai.ChatCompletion.acreate(
            model=engine,
            prompt=prompt,
            max_tokens=2500,
            n=1,
            temperature=0.5,
            request_timeout=self.request_timeout,
        )
        return completions.choices[0].text.strip()
