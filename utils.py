import asyncio

def async_retry(num_retries=3, exceptions=(Exception,), delay=0.1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for i in range(num_retries):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except exceptions as e:
                    if i == num_retries - 1:
                        raise e
                    await asyncio.sleep(delay)
        return wrapper
    return decorator