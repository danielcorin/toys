# Sandboxed Python

Using Docker to run potentially unsafe Python libraries in an isolated environment.

Code for [this blog post](https://github.com/danielcorin/blog/blob/main/content/posts/2024/sandboxed-python-env.md)

[Live article](https://www.danielcorin.com/posts/2024/sandboxed-python-env/)

## Setup

```sh
cp .env.template .env
# add your api key to .env
```

Add dependencies to `requirements.txt`.

Modify `run.py` and add the code you want to run sandboxed.

Run with `make run`.
