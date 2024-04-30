import asyncio
import uuid

from constants import WORKFLOW_TASK_QUEUE
from temporalio.client import Client
from workflows import MyGoodWorkflow, MyGoodWorkflowArgs, MyGoodWorkflowResult

async def main() -> MyGoodWorkflowResult:
    client = await Client.connect("localhost:7233")

    result: MyGoodWorkflowResult = await client.execute_workflow(
        MyGoodWorkflow.run,
        MyGoodWorkflowArgs(
            arg1=f"workflow arg1",
            arg2="workflow arg2",
        ),
        id=str(uuid.uuid4()),
        task_queue=WORKFLOW_TASK_QUEUE,
    )

    print(f"Workflow completed with result: {result}")
    return result

if __name__ == "__main__":
    asyncio.run(main())
