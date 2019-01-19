import asyncio
import pygame
import websockets
import time

import game

(width,height) = (game.width, game.height)

async def render_game():
    global width
    global height
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    frame_rate = 30

    while running:
        cur_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill([255,255,255])

        for p in game.universe.planets:
            pygame.draw.circle(screen, [0,0,0], (int(p.position.x), int(p.position.y)), p.radius)

        pygame.display.flip()
        await asyncio.sleep(time.time()-cur_time + 1/frame_rate)

async def sendData(websocket, path):
    global universe
    print(universe.width)
    while True:
        #data = somefunct()
        await websocket.send(data)
        await asyncio.sleep(0.04)

start_server = websockets.serve(sendData, 'localhost', 8765)

loop = asyncio.get_event_loop()
loop.create_task(game.physics_loop())
loop.create_task(render_game())
#loop.create_task(start_server)
loop.run_forever()

