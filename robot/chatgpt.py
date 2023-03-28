import openai

import config
import utils

from rebot import Rebot

class Chat_gpt(Rebot):
    def __init__(self) -> None:
        super().__init__()

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt(self, question):
        prompt = question
        model_engine = "text-davinci-003"
        completions = await openai.Completion.acreate(
               engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print(completions)
        return completions.choices[0].text

    @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt_context(self, question, args):
        args.reverse()
        args.append(question)
        prompt = '\n'.join(args)[-1500:]
        completions = await openai.Completion.acreate(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=2500,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return completions.choices[0].text.strip()
