from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
    
def get_grok_response(messages, model="grok-3"):
    """
    Get a response from the xAI API based on a conversation history.
    
    Args:
        messages (list): A list of message dictionaries representing the conversation history.
        model (str): The Grok model to use.
        
    Returns:
        str: The API response.
    """
    try:
        # Configure the client to use the xAI API
        client = OpenAI(
          api_key=os.getenv("XAI_API_KEY"),
          base_url="https://api.x.ai/v1",
        )
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages  # Send the entire conversation history
            
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# This file is now a module. 
# The main chat logic has been moved to agent.py.