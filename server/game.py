from engine import Universe
import time
import asyncio
import pygame

radius = 450
(width, height) = (2*radius,2*radius)
physics_rate = 500

universe = Universe(radius, 1/physics_rate)

competition_mode = True
game_active = not competition_mode

async def physics_loop():
    while True:
        cur_time = time.time()
        if game_active: universe.run_loop()
        await asyncio.sleep(1/physics_rate - time.time() + cur_time)


async def render_loop():
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    frame_rate = 30

    physics_time = time.time()

    while running:
        cur_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        while (physics_time + 1/physics_rate < time.time()):
            universe.run_loop()
            physics_time += 1/physics_rate

        screen.fill([255,255,255])

        for p in universe.planets:
            pygame.draw.circle(screen, [0,0,0], (int(p.position.x), int(p.position.y)), p.radius)

        pygame.display.flip()
        await asyncio.sleep(1/frame_rate - time.time() + cur_time)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(render_game())
