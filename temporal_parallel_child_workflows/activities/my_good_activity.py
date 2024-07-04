import random

from dataclasses import dataclass
from temporalio import activity


@dataclass
class MyGoodActivityArgs:
    arg1: str
    arg2: str


@dataclass
class MyGoodActivityResult:
    arg1: str
    arg2: str
    random_val: float


@activity.defn
async def my_good_activity(args: MyGoodActivityArgs) -> MyGoodActivityResult:
    activity.logger.info("Running my good activity")
    return MyGoodActivityResult(
        arg1=args.arg1,
        arg2=args.arg2,
        random_val=random.random(),
    )
