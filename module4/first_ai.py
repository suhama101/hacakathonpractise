from groq import Groq
from dotenv import load_dotenv,find_dotenv
import os

load_dotenv()(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Pakistan ki capital kya hai?"}]
)

print(response.choices[0].message.content)