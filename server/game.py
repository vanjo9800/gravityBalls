import pygame
from engine import Universe
import time
import asyncio

(width, height) = (600,600)
screen = pygame.display.set_mode((width, height))

frame_rate = 30
physics_rate = 250

universe = Universe(width, height, 1/physics_rate)

async def physics_loop():
    global universe
    running = True
    clock = pygame.time.Clock()

    frame_time = time.time()
    physics_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while (time.time() > physics_time + 1/physics_rate):
            physics_time += 1/physics_rate
            universe.run_loop()

        screen.fill([255,255,255])

        for p in universe.planets:
            pygame.draw.circle(screen, [0,0,0], (int(p.position.x), int(p.position.y)), p.radius)

        pygame.display.flip()
        clock.tick(frame_rate)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(physics_loop())

