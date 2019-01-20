import sys
import asyncio
import websockets
import time

import game

send_rate = 20

users = set()

async def consumer_handler(websocket, path, pid):
    try:
        async for message in websocket:
            if pid >= 0:
                if message == "+": game.universe.grow(pid)
                if message == "-": game.universe.shrink(pid)
            if message == "s":
                if not game.game_active and len(users) > 1:
                    game.game_active = True
    except websockets.exceptions.ConnectionClosed:
        pass

async def producer_handler(websocket, path):
    cur_game_active = False
    try:
        while True:
            cur_time = time.time()
            if not cur_game_active and game.game_active:
                await websocket.send("s")
                cur_game_active = game.game_active

            await websocket.send(game.universe.get_json())
            await asyncio.sleep(1/send_rate - time.time() + cur_time)
    except websockets.exceptions.ConnectionClosed:
        pass

async def handler(websocket, path):
    if not game.game_active:
        pid = game.universe.add_planet()
        users.add(pid)
    else: pid = -1

    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path, pid))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
    
    game.universe.remove_planet(pid)
    users.discard(pid)
    if game.competition_mode and len(users) == 0:
        game.game_active = False


start_server = websockets.serve(handler, '', 8765)

if len(sys.argv) > 1 and "-visual" in sys.argv[1:]:
    game_loop = game.render_loop()
else:
    game_loop = game.physics_loop()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(start_server, game_loop))

