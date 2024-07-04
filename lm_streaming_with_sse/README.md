# Language model streaming with SSE

How to stream and display results from language model inferences to a UI in real-time

Code for [this blog post](https://github.com/danielcorin/blog/blob/main/content/posts/2024/lm-streaming-with-sse.md)

[Live article](https://www.danielcorin.com/posts/2024/lm-streaming-with-sse/)

## Setup

```sh
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Run

```sh
uvicorn server:app --reload
```

Load site at http://localhost:8000
