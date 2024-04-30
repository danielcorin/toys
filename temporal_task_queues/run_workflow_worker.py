import asyncio

from constants import WORKFLOW_TASK_QUEUE
from workflows import MyGoodWorkflow
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(
      client,
      task_queue=WORKFLOW_TASK_QUEUE,
      workflows=[MyGoodWorkflow],
    )
    await worker.run()

if __name__ == "__main__":
    print("Starting workflow worker")
    asyncio.run(main())
