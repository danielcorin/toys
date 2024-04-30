# Temporal Task Queues

This is a small project showing how to run Temporal workflows and activities with separate workers for a single workflow run.

## Setup

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Temporal server

### Install

On macOS

```sh
brew install temporal
```

### Run it

```sh
temporal server start-dev
```

## Start the workers

```sh
python -m run_workflow_worker
```

```sh
python -m run_activity_worker
```

## Run the workflow

```sh
python -m run_workflow
#=> Workflow completed with result: MyGoodWorkflowResult(result='Ran my good activity for args: activity arg1: workflow arg1, activity arg2: workflow arg2')
```

## Add a new dependency

Install [`uv`](https://github.com/astral-sh/uv) which we use as a pip-tools substitute.

```sh
pip install uv
```

Add dependency to `requirements.in`.

Re-compile `requirements.txt` file:

```sh
uv pip compile requirements.in -o requirements.txt
```
