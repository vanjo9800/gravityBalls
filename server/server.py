import sys
import asyncio
import websockets
import time

import game

send_rate = 30

async def consumer_handler(websocket, path, pid):
    async for message in websocket:
        if message == "+": game.universe.grow(pid)
        if message == "-": game.universe.shrink(pid)

async def producer_handler(websocket, path):
    try:
        while True:
            cur_time = time.time()
            await websocket.send(game.universe.get_json())
            await asyncio.sleep(1/send_rate - time.time() + cur_time)
    except websockets.exceptions.ConnectionClosed:
        print("closing")
        pass

async def handler(websocket, path):
    pid = game.universe.add_planet()

    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path, pid))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
    
    game.universe.remove_planet(pid)


start_server = websockets.serve(handler, '', 8765)

if len(sys.argv) > 1 and sys.argv[1] == "-visual":
    game_loop = game.render_loop()
else:
    game_loop = game.physics_loop()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(start_server, game_loop))

