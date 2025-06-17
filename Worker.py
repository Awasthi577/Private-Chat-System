import asyncio

running_jobs = {}

async def rotate_keys():
    while True:
        print("Rotating identity/prekeys...")
        await asyncio.sleep(30)  # simulate task duration

async def maintain_connection():
    while True:
        print("Maintaining secure socket to relay...")
        await asyncio.sleep(15)

async def start_job(name, coro):
    if name in running_jobs:
        print(f"Job {name} already running.")
        return
    task = asyncio.create_task(coro())
    running_jobs[name] = task
    print(f"Started job: {name}")

async def shutdown_jobs():
    print("Shutting down jobs...")
    for name, task in running_jobs.items():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print(f"Cancelled: {name}")
