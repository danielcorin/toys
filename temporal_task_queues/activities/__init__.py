from dataclasses import dataclass
from temporalio import activity


@dataclass
class MyGoodActivityArgs:
    arg1: str
    arg2: str


@activity.defn
async def my_good_activity(args: MyGoodActivityArgs) -> str:
    print("Running my good activity")
    return f"Ran my good activity for args: {args.arg1}, {args.arg2}"
