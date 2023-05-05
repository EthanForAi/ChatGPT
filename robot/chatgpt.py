import openai

from robot import robot

engine = "gpt-3.5-turbo"
davinci_engine = "text-davinci-003"

class Chat_gpt(robot):
    def __init__(self) -> None:
        super().__init__()
        self.request_timeout = 60

    # @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt(self, question):
        prompt = question
        completions = await openai.Completion.acreate(
            engine=engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.5,
            request_timeout=self.request_timeout,
        )
        return completions.choices[0].text

    # @utils.async_retry(num_retries=3, delay=0.1)
    async def ask_chat_gpt_context(self, question, args):
        args.reverse()
        args.append(question)
        prompt = '\n'.join(args)[-1000:]
        completions = await openai.Completion.acreate(
            engine=engine,
            prompt=prompt,
            max_tokens=2500,
            n=1,
            temperature=0.5,
            request_timeout=self.request_timeout,
        )
        return completions.choices[0].text.strip()
