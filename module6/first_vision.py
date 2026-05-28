from groq import Groq
from dotenv import load_dotenv
import os
import base64

load_dotenv(r"C:\Users\Suhama\Desktop\Hackathon\.env")
client = Groq(api_key=os.getenv("GROQ_KEY"))

def analyze_image(image_path, question):
    # Image ko base64 mein convert karo
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Extension se format nikalo
    ext = image_path.split(".")[-1].lower()
    if ext == "jpg":
        ext = "jpeg"
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{ext};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )
    
    return response.choices[0].message.content

# Test — koi bhi image rakh do module6 mein
result = analyze_image("test.jpg", "Is image mein kya hai? Urdu/English mein batao.")
print(result)