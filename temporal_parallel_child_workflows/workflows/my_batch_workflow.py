import asyncio
from dataclasses import dataclass
from typing import List

from constants import TASK_QUEUE
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from workflows.my_good_workflow import (
        MyGoodWorkflow,
        MyGoodWorkflowArgs,
        MyGoodWorkflowResult,
    )


@dataclass
class BatchWorkflowArgs:
    inputs: List[MyGoodWorkflowArgs]


@dataclass
class BatchWorkflowResult:
    results: List[MyGoodWorkflowResult]


@workflow.defn
class MyBatchWorkflow:
    @workflow.run
    async def run(self, args: BatchWorkflowArgs) -> BatchWorkflowResult:
        # Create a list to store the workflow futures
        workflow_futures = []

        # Create child workflow stubs for each set of args
        for i, workflow_args in enumerate(args.inputs):
            future = await workflow.start_child_workflow(
                MyGoodWorkflow,
                workflow_args,
                id=f"my_good_workflow_{i}",
                task_queue=TASK_QUEUE,
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            workflow_futures.append(future)

        # Wait for all workflows to complete and collect results
        results: List[MyGoodWorkflowResult] = await asyncio.gather(*workflow_futures)

        workflow.logger.info(
            f"Completed {len(workflow_futures)} MyGoodWorkflow workflows"
        )

        return BatchWorkflowResult(results)
