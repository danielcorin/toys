import asyncio
import uuid

from constants import TASK_QUEUE
from temporalio.client import Client
from workflows.my_batch_workflow import (
    BatchWorkflowArgs,
    MyBatchWorkflow,
    BatchWorkflowResult,
)
from workflows.my_good_workflow import MyGoodWorkflowArgs


async def main() -> BatchWorkflowResult:
    client = await Client.connect("localhost:7233")

    batch_args = BatchWorkflowArgs(
        inputs=[
            MyGoodWorkflowArgs(arg1="workflow arg1", arg2="workflow arg2"),
            MyGoodWorkflowArgs(arg1="workflow arg3", arg2="workflow arg4"),
        ]
    )

    result: BatchWorkflowResult = await client.execute_workflow(
        MyBatchWorkflow.run,
        batch_args,
        id=str(uuid.uuid4()),
        task_queue=TASK_QUEUE,
    )

    print(f"Batch workflow completed with results: {result}")
    return result


if __name__ == "__main__":
    asyncio.run(main())
