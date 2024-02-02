import json
import os
from typing import Optional, Type

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()

CHAT_SYSTEM_PROMPT = "You are a thoughtful assistant that asks the user followup questions about their idea. Ask only one follow up question at a time."

EXTRACTION_SYSTEM_PROMPT = """You will analyze a conversation between a language model and a user.
The conversation between the user and the model is about a document that the model will help the user write.
You goal is to extract the following information that relates to the document that the user and the model will collaborate on from the conversation in adherence with the following schema:
{schema}

You have already extracted the following data:
{data}

Output JSON in adherence to the schema, extraction the information that has been provided by the conversation.
"""

class ContentContext(BaseModel):
    topic: Optional[str] = Field(
        description="The main subject matter or theme of the content being created.",
        default=None,
    )
    audience: Optional[str] = Field(
        description="The intended target group for whom the content is being written.",
        default=None,
    )
    purpose: Optional[str] = Field(
        description="The underlying reason or objective behind the creation of the content.",
        default=None,
    )


context = ContentContext()


chat_messages = [
    {
        "role": "system",
        "content": CHAT_SYSTEM_PROMPT,
    },
    {
        "role": "assistant",
        "content": "What would you like to write about?",
    },
]


def get_completion(messages, model="gpt-4-1106-preview") -> str:
    completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return completion.choices[0].message.content

def get_completion_object(completion: str, cls: Type[BaseModel]) -> BaseModel:
    result_obj: dict = json.loads(completion)
    return cls.model_validate(result_obj)

def chat(msg: str):
    chat_messages.append({
        "role": "user",
        "content": msg,
    })
    bot_response = get_completion(chat_messages)
    chat_messages.append({
        "role": "assistant",
        "content": bot_response,
    })
    print_chat(chat_messages)

def extract(messages, context: BaseModel):
    prompt = EXTRACTION_SYSTEM_PROMPT.format(
        schema=type(context).model_json_schema(),
        data=context.model_dump_json(),
    )
    extract_messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": f"Here is the conversation:\n{chat_string(messages)}"
        }
    ]
    completion = get_completion(extract_messages)
    context = get_completion_object(completion, type(context))
    return context


def chat_string(messages):
    return '\n'.join([f'{m["role"]}: {m["content"]}' for m in messages])

def print_chat(messages):
    print(chat_string(messages))


def main():
    print_chat(chat_messages)
    while True:
        msg = input("> ")
        chat(msg)
        print(extract(chat_messages, context))

if __name__ == "__main__":
    main()
