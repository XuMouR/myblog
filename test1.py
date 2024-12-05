import asyncio

async def task(name, delay):
        print(f"Task {name} started")
        await asyncio.sleep(delay)
        print(f"Task {name} finished")

async def main():
        await asyncio.ga(
        task("A", 2),
        task("B", 1),
        task("C", 3
        ))