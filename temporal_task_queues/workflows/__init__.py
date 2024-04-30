from dataclasses import dataclass
from datetime import timedelta
from activities import MyGoodActivityArgs
from constants import ACTIVITY_TASK_QUEUE
from temporalio import workflow


@dataclass
class MyGoodWorkflowArgs:
    arg1: str
    arg2: str

@dataclass
class MyGoodWorkflowResult:
    result: str

with workflow.unsafe.imports_passed_through():
    from activities import my_good_activity

@workflow.defn
class MyGoodWorkflow:
    @workflow.run
    async def run(self, args: MyGoodWorkflowArgs) -> MyGoodWorkflowResult:
        result: str = await workflow.execute_activity(
            my_good_activity,
            MyGoodActivityArgs(
                arg1=f"activity arg1: {args.arg1}",
                arg2=f"activity arg2: {args.arg2}",
            ),
            schedule_to_close_timeout=timedelta(seconds=5),
            task_queue=ACTIVITY_TASK_QUEUE,
        )
        return MyGoodWorkflowResult(result=result)
