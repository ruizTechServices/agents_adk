import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_response(prompt, model="gpt-4.1"):
    """
    Get a response from OpenAI API.
    
    Args:
        prompt (str): The user's input prompt
        model (str): The OpenAI model to use
        
    Returns:
        str: The API response
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    user_input = input("Type your question: ")
    result = get_openai_response(user_input)
    print(result)

# How to use in other files:
# 
# 1. Import the function:
# from openai_service import get_openai_response
# 
# 2. Use the function:
# response = get_openai_response("What is the capital of France?")
# print(response)
