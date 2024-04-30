import asyncio
import concurrent.futures

from activities import my_good_activity
from constants import ACTIVITY_TASK_QUEUE
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    client = await Client.connect("localhost:7233")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=ACTIVITY_TASK_QUEUE,
            workflows=[],
            activities=[my_good_activity],
            activity_executor=activity_executor,
        )
        await worker.run()

if __name__ == "__main__":
    print("Starting activity worker")
    asyncio.run(main())
