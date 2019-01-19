import asyncio
import websockets
import time

import game

send_rate = 1

async def consumer_handler(websocket, path):
    async for message in websocket:
        print(message)

async def producer_handler(websocket, path):
    while True:
        cur_time = time.time()
        await websocket.send(game.universe.get_json())
        await asyncio.sleep(1/send_rate - time.time() + cur_time)

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


start_server = websockets.serve(handler, 'localhost', 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(start_server, game.render_game()))

