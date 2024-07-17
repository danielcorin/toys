import anthropic
import base64
import os
import sys


class LLMGateway:
    def _image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def send_message(self, prompt: str, image: str, system: str = "") -> str:
        raise NotImplementedError("This method should be implemented by subclasses")


class AnthropicGateway(LLMGateway):
    def __init__(self, model):
        self.client = anthropic.Anthropic()
        self.model = model

    def send_message(self, prompt: str, image: str, system: str = "") -> str:
        content = [{"type": "text", "text": prompt}]

        if image:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": self._image_to_base64(image),
                    },
                }
            )

        messages = [{"role": "user", "content": content}]

        completion = self.client.messages.create(
            model=self.model,
            system=system,
            messages=messages,
            temperature=0,
            max_tokens=4095,
        )
        return completion.content[0].text


class LLMService:
    def __init__(self, gateway: LLMGateway):
        self.gateway = gateway

    def process_image(self, prompt: str, image_path: str, system: str = "") -> str:
        return self.gateway.send_message(prompt, image_path, system)

    def process_prompt(self, prompt: str, system: str = ""):
        return self.gateway.send_message(prompt, "", system)


def main(image_folder, prompt):
    anthropic_gateway = AnthropicGateway(model="claude-3-5-sonnet-20240620")
    llm_service = LLMService(anthropic_gateway)

    all_image_paths = {}

    for folder in os.listdir(image_folder):
        folder_path = os.path.join(image_folder, folder)
        if os.path.isdir(folder_path):
            all_image_paths[folder] = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(".png"):
                    image_path = os.path.join(folder_path, file)
                    all_image_paths[folder].append(image_path)

    results = {}
    total_correct = 0
    total_images = 0
    failed_images = {}

    for expected_count, image_paths in all_image_paths.items():
        results[expected_count] = {"correct": 0, "total": len(image_paths)}
        failed_images[expected_count] = []
        for image_path in image_paths:
            print(image_path)
            response = llm_service.process_image(
                prompt,
                image_path,
            )
            print(response)
            count_check = llm_service.process_prompt(
                response,
                system="Given the output of another language model, output a number denoting how many times the lines intersected according to the model. Remember, output a single number only!",
            )
            print(count_check)

            try:
                predicted_count = int(count_check.strip())
                if predicted_count == int(expected_count):
                    results[expected_count]["correct"] += 1
                    total_correct += 1
                else:
                    failed_images[expected_count].append(image_path)
            except ValueError:
                failed_images[expected_count].append(image_path)

            total_images += 1

    # Calculate accuracy for each category and overall
    for expected_count, result in results.items():
        result["accuracy"] = (
            result["correct"] / result["total"] if result["total"] > 0 else 0
        )

    overall_accuracy = total_correct / total_images if total_images > 0 else 0

    # Print summary
    print("Results summary:")
    for expected_count, result in results.items():
        print(
            f"Expected count {expected_count}: {result['correct']}/{result['total']} correct (Accuracy: {result['accuracy']:.2%})"
        )
        if failed_images[expected_count]:
            print(f"Failed images for count {expected_count}:")
            for failed_image in failed_images[expected_count]:
                print(f"  - {failed_image}")
    print(f"Overall accuracy: {overall_accuracy:.2%}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run.py <image_folder> <prompt>")
        sys.exit(1)

    image_folder = sys.argv[1]
    prompt = sys.argv[2]
    if prompt == "p1":
        prompt = "How many times do the blue and red line intersect?"
    else:
        prompt = "How many times do the blue and red line plots cross each other?"

    if not os.path.isdir(image_folder):
        print(f"Error: {image_folder} is not a valid directory")
        sys.exit(1)

    main(image_folder, prompt)
