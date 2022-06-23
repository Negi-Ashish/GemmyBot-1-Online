import os
import asyncio
from gemmyBot1 import client
from gemmyTestBot import client2
import config.constants as const;
  
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(const.BOT_TOKEN))
    loop.create_task(client2.start(const.TEST_BOT_TOKEN))
    loop.run_forever()
