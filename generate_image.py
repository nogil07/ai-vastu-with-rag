import os
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def _save_image_from_response(image_data, output_path: str) -> bool:
    # gpt-image responses can return URL or base64 depending on account/settings.
    if getattr(image_data, "url", None):
        img_data = requests.get(image_data.url, timeout=60).content
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
        return True

    if getattr(image_data, "b64_json", None):
        img_bytes = base64.b64decode(image_data.b64_json)
        with open(output_path, 'wb') as handler:
            handler.write(img_bytes)
        return True

    return False


def main():
    """
    Reads the optimized prompt from disk, calls image generation, and saves output.
    Returns True if successful.
    """
    prompt_file = "optimized_prompt_output.txt"
    output_file = "generated_floor_plan.png"

    if not os.path.exists(prompt_file):
        print(f"Error: {prompt_file} not found.")
        return False

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()

    if not prompt:
        print("Error: Prompt is empty.")
        return False

    apikey = os.getenv("OPENAI_API_KEY")
    if not apikey:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return False

    client = OpenAI(api_key=apikey)

    print("\nSending prompt to image model (usually 10-30 seconds)...")
    try:
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size="1536x1024",
            quality="auto",
            n=1,
        )

        if not response.data or len(response.data) == 0:
            print("Error: No image returned by API.")
            return False

        saved = _save_image_from_response(response.data[0], output_file)
        if not saved:
            print("Error: API returned image payload in an unsupported format.")
            return False

        print(f"Saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating image: {e}")
        return False


if __name__ == "__main__":
    main()
