import asyncio

from constants import TASK_QUEUE
from activities.my_good_activity import my_good_activity
from workflows.my_batch_workflow import MyBatchWorkflow
from workflows.my_good_workflow import MyGoodWorkflow
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[MyGoodWorkflow, MyBatchWorkflow],
        activities=[my_good_activity],
    )
    await worker.run()


if __name__ == "__main__":
    print("Starting workflow worker")
    asyncio.run(main())
