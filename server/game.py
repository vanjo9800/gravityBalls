from engine import Universe
import time
import asyncio

(width, height) = (600,600)
physics_rate = 250

universe = Universe(width, height, 1/physics_rate)

async def physics_loop():
    global universe
    global physics_rate

    while True:
        cur_time = time.time()
        universe.run_loop()
        await asyncio.sleep(cur_time + 1/physics_rate - time.time())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(physics_loop())
