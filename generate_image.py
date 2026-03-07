import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Reads the optimized prompt from disk, calls DALL-E 3 to generate a 2D floor plan,
    and saves the resulting image to disk. Returns True if successful.
    """
    prompt_file = "optimized_prompt_output.txt"
    if not os.path.exists(prompt_file):
        print(f"Error: {prompt_file} not found.")
        return False

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read()

    apikey = os.getenv("OPENAI_API_KEY")
    if not apikey:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return False

    client = OpenAI(api_key=apikey)
    
    print("\nSending prompt to DALL-E 3 (This usually takes 10-20 seconds)...")
    try:
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        print("Image generated successfully! Downloading...")
        
        img_data = requests.get(image_url).content
        with open('generated_floor_plan.png', 'wb') as handler:
            handler.write(img_data)
            
        print("Saved to generated_floor_plan.png")
        return True
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

if __name__ == "__main__":
    main()
