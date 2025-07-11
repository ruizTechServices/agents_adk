import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_response(messages, model="gpt-4o-mini"):
    """
    Get a response from OpenAI API based on a conversation history.
    
    Args:
        messages (list): A list of message dictionaries representing the conversation history.
        model (str): The OpenAI model to use.
        
    Returns:
        str: The API response.
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=messages  # Send the entire conversation history
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# This file is now a module. 
# The main chat logic has been moved to agent.py.