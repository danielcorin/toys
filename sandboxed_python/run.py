import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

stream = client.chat.completions.create(
  messages=[
    {
      "role": "system",
      "content": "You are an AI assistant",
    },
    {
      "role": "user",
      "content": "What is the best thing about New York City? Pick only one.",
    }
  ],
  model="gpt-3.5-turbo",
  stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
