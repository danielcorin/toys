import argparse
import base64
import google.generativeai as genai
import importlib
import json
import logging
import os
from pathlib import Path
from typing import Any, List, Optional
import httpx

from google.protobuf.json_format import Parse
from openai import OpenAI
import anthropic
import fitz  # PyMuPDF
from PIL import Image
import io

logger = logging.getLogger(__name__)

PROMPT = """```proto{schema}
```

Using the provided content and images, extract an instance of `{target_obj}` as JSON in adherence to the above schema.
No talk. JSON only. Adhere to any comments or annotations - those are instructions for you.
"""


class FileContainer:
    def __init__(self):
        self.pages: List[bytes] = []
        self.image_type: str = "jpeg"

    def add_page(self, page_bytes: bytes):
        self.pages.append(page_bytes)

    def set_image_type(self, image_type: str):
        if image_type.lower() == "jpg":
            self.image_type = "jpeg"
        else:
            self.image_type = image_type


def unpack_json_to_proto(json_data: str, target_obj: str, module) -> Any:
    """
    Unpacks JSON data into a protobuf object.

    Args:
    json_data (str): JSON string to unpack.
    target_obj (str): Name of the protobuf class.
    module: The dynamically imported protobuf module.

    Returns:
    Any: An instance of the specified protobuf class with data from the JSON.
    """
    # Get the protobuf class from the module
    proto_class = getattr(module, target_obj)

    # Parse JSON string to dict
    data_dict = json.loads(json_data)

    # Create a new instance of the protobuf class
    proto_instance = proto_class()

    # Use the Parse function to populate the protobuf instance
    Parse(json.dumps(data_dict), proto_instance)

    return proto_instance


def main(proto: str, file_path: str, model: str = "openai") -> None:
    # Read the proto file
    path, target_obj = proto.split(":")
    proto_path = Path(path)
    with proto_path.open("r") as proto_file:
        schema = proto_file.read()

    # Dynamically import the generated code
    module_name = proto_path.stem + "_pb2"
    gen_path = Path("gen") / proto_path.relative_to(proto_path.anchor)
    gen_path = gen_path.with_name(module_name + ".py")
    spec = importlib.util.spec_from_file_location(module_name, str(gen_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Now we can use the imported module and the schema
    file_container = process_file(file_path)
    result = extract_from_file_container(file_container, schema, target_obj, model)
    result = result.strip().removeprefix("```json").removesuffix("```")
    logger.info("Extracted JSON:")
    logger.info(result)

    if result:
        proto_instance = unpack_json_to_proto(result, target_obj, module)
        logger.info("Proto instance:")
        logger.info(proto_instance)
    return proto_instance


def process_file(file_path: str) -> FileContainer:
    file_container = FileContainer()

    if file_path.lower().startswith(("http://", "https://")):
        with httpx.Client() as client:
            response = client.get(file_path)
            response.raise_for_status()
            content = response.content
        image_type = Path(file_path).suffix[1:] or "jpeg"
        file_container.add_page(content)
        file_container.set_image_type(image_type)
    elif file_path.lower().endswith(".pdf"):
        pdf_document = fitz.open(file_path)
        for page in pdf_document:
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG", quality=100)
            file_container.add_page(buffer.getvalue())
        pdf_document.close()
        file_container.set_image_type("png")
    else:
        with open(file_path, "rb") as image_file:
            content = image_file.read()
        img = Image.open(io.BytesIO(content))
        img = img.resize(
            (img.width * 2, img.height * 2), Image.LANCZOS
        )  # Double the resolution
        buffer = io.BytesIO()
        img.save(buffer, format=img.format, quality=100)
        high_res_content = buffer.getvalue()
        file_container.add_page(high_res_content)
        file_container.set_image_type(Path(file_path).suffix[1:])

    return file_container


def extract_from_file_container(
    file_container: FileContainer, schema: str, target_obj: str, model: str
) -> Optional[str]:
    if model == "openai":
        return extract_from_file_container_openai(file_container, schema, target_obj)
    elif model == "anthropic":
        return extract_from_file_container_anthropic(file_container, schema, target_obj)
    elif model == "gemini":
        return extract_from_file_container_gemini(file_container, schema, target_obj)
    else:
        raise ValueError(f"Unsupported model: {model}")


def extract_from_file_container_openai(
    file_container: FileContainer, schema: str, target_obj: str
) -> Optional[str]:
    # Initialize the OpenAI client
    client = OpenAI()

    # Encode the images
    encoded_images = [
        base64.b64encode(img).decode("utf-8") for img in file_container.pages
    ]

    # Prepare the content for the API call
    content = [
        {
            "type": "text",
            "text": PROMPT.format(schema=schema, target_obj=target_obj),
        }
    ]
    for encoded_image in encoded_images:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{file_container.image_type};base64,{encoded_image}"
                },
            }
        )

    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]
    # Make the API call to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
        )

        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"An error occurred during OpenAI API call: {e}")
        return None


def extract_from_file_container_anthropic(
    file_container: FileContainer, schema: str, target_obj: str
) -> Optional[str]:
    # Initialize the Anthropic client
    client = anthropic.Anthropic()

    # Prepare the content for the API call
    content = PROMPT.format(schema=schema, target_obj=target_obj)
    messages = [
        {"type": "text", "text": content},
        *[
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": f"image/{file_container.image_type}",
                    "data": base64.b64encode(img).decode("utf-8"),
                },
            }
            for img in file_container.pages
        ],
    ]

    # Make the API call to Anthropic
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": messages,
                }
            ],
        )

        return response.content[0].text
    except Exception as e:
        logger.error(f"An error occurred during Anthropic API call: {e}")
        return None


def extract_from_file_container_gemini(
    file_container: FileContainer,
    schema: str,
    target_obj: str,
) -> Optional[str]:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    content = PROMPT.format(schema=schema, target_obj=target_obj)

    # Prepare image parts
    image_parts = [
        {"mime_type": f"image/{file_container.image_type}", "data": img}
        for img in file_container.pages
    ]

    parts = [{"text": content}] + image_parts

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(parts)

        return response.text
    except Exception as e:
        logger.error(f"An error occurred during Gemini API call: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a receipt from an image or PDF."
    )
    parser.add_argument("--proto", type=str, help="The proto file path", required=True)
    parser.add_argument(
        "--file_path",
        type=str,
        help="Path to the receipt image or PDF, or URL to download from",
        required=True,
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["openai", "anthropic", "gemini"],
        default="openai",
        help="The model to use for extraction (openai or anthropic)",
    )
    parser.add_argument(
        "--log_level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level",
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    main(args.proto, args.file_path, args.model)
