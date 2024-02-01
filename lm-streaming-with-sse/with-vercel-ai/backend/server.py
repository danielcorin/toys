from openai import AsyncOpenAI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# Added because the frontend and this backend run on separate ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI()

@app.post('/ask')
async def ask(req: dict):
    stream = await client.chat.completions.create(
        messages=req["messages"],
        model="gpt-3.5-turbo",
        stream=True,
    )

    async def generator():
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    response_messages = generator()
    return StreamingResponse(response_messages, media_type='text/event-stream')
