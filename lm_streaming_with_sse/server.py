from openai import AsyncOpenAI
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse


app = FastAPI()
client = AsyncOpenAI()

async def generator(msg: str):
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,
    )

    async for chunk in stream:
        s = chunk.choices[0].delta.content or ""
        s = s.replace("\n", "\r")
        yield f"data: {s}\n\n"
    yield f"data: [DONE]\n\n"


@app.get("/ask")
async def main(msg):
    return StreamingResponse(generator(msg), media_type="text/event-stream")


@app.get("/")
async def get_index():
    return FileResponse("index.html")
