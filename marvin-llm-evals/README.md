# Marvin LLM evals

Code for
[this blog post](https://github.com/danielcorin/blog/blob/main/content/posts/2024/evals-unit-testing-for-lms.md)

[Live article](https://www.danielcorin.com/posts/2024/evals-unit-testing-for-lms/)

This repo contains examples of a unit test-based approach to run LLM evals. It
uses Prefect's library [`marvin`](https://github.com/prefecthq/marvin), a
"lightweight AI toolkit", to demonstrate a few eval approaches (and abuses).

## Setup

```sh
make install
```

## Add a new dependency

Install [`uv`](https://github.com/astral-sh/uv) which we use as a pip-tools
substitute.

```sh
pip install uv
```

Add dependency to `requirements.in`.

Re-compile `requirements.txt` file:

```sh
uv pip compile requirements.in -o requirements.txt
```

## Run

```sh
pytest test.py
```
