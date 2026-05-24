# Yeh hata do:
client = Groq(api_key="gsk_XXXX...")

# Yeh lagao uski jagah:
from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_KEY"))

messages = [
    {"role": "system", "content": "Tum ek helpful Pakistani AI assistant ho. Simple aur clear jawab do."}
]

print("🤖 AI Chatbot Ready! 'quit' likhne se band hoga")
print("=" * 40)

while True:
    user_input = input("\nTum: ")
    
    if user_input.lower() == "quit":
        print("Khuda Hafiz!")
        break
    
    if user_input.strip() == "":
        continue
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        
        answer = response.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        
        print(f"\nAI: {answer}")
        
    except Exception as e:
        print(f"❌ Error: {e}")