import asyncio
import websockets

async def sendData(websocket, path):
    while True:
        #data = somefunct()
        await websocket.send(data)
        await asyncio.sleep(0.04)

start_server = websockets.serve(sendData, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()