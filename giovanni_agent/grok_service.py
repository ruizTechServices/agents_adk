# from openai import OpenAI
    
# client = OpenAI(
#   api_key=XAI_API_KEY,
#   base_url="https://api.x.ai/v1",
# )

# completion = client.chat.completions.create(
#   model="grok-3",
#   messages=[
#     {"role": "user", "content": "What is the meaning of life, the universe, and everything?"}
#   ]
# )

import os

from xai_sdk import Client
from xai_sdk.chat import user, system

client = Client(api_key=os.getenv("XAI_API_KEY"))

chat = client.chat.create(model="grok-4")
chat.append(system("You are Grok, a highly intelligent, helpful AI assistant."))
chat.append(user("What is the meaning of life, the universe, and everything?"))

response = chat.sample()
print(response.content)