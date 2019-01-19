import asyncio
import websockets

import game

async def sendData(websocket, path):
    global universe
    print(universe.width)
    while True:
        #data = somefunct()
        await websocket.send(data)
        await asyncio.sleep(0.04)

start_server = websockets.serve(sendData, 'localhost', 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(game.render_game()))

