# Temporal Parallel Child Workflows

Using Temporal to execute multiple child workflows concurrently within a parent workflow

Code for [this blog post]()

[Live article](https://www.danielcorin.com/til/temporal/parallel-child-workflows/)

## Setup

```sh
make install
```

## Run

Start local Temporal server

```sh
make temporal-server
```

Start Temporal worker

```sh
make temporal-worker
```

Run batch workflow

```sh
make run-workflow
```

### Example results

```sh
❯ make run-workflow
python -m run_workflow
Batch workflow completed with results: [MyGoodWorkflowResult(result=MyGoodActivityResult(arg1='activity arg1: workflow arg1', arg2='activity arg2: workflow arg2', random_val=0.9148414577193964)), MyGoodWorkflowResult(result=MyGoodActivityResult(arg1='activity arg1: workflow arg3', arg2='activity arg2: workflow arg4', random_val=0.01852280671355544))]
```

## Add a new dependency

Add dependency to `requirements.in`.

Re-compile `requirements.txt` file:

```sh
make compile
```

Reinstall dependencies

```sh
make install
```
