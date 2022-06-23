import os
import asyncio
from gemmyBot1 import client
from gemmyTestBot import client2
from botOneDB import app
import config.constants as const;
from threading import Thread



def Task1():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(const.BOT_TOKEN))
    loop.create_task(client2.start(const.TEST_BOT_TOKEN))
    loop.run_forever()

def Task2():
    app.run(debug=False)

if __name__ == "__main__":
    t1 = Thread(target=Task1)
    t2 = Thread(target=Task2)

    t1.start()
    t2.start()
