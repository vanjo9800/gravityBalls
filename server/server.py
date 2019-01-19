import asyncio
import websockets

import game

async def sendData(websocket, path):
    print(game.universe.width)
    try:
        while True:
            await websocket.send(game.universe.get_json())
            await asyncio.sleep(0.02)
    except websockets.exceptions.ConnectionClosed:
        print("closed")
    finally:
        websocket.close()



start_server = websockets.serve(sendData, 'localhost', 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(start_server, game.render_game()))

