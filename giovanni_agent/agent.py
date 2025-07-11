from google.adk.agents import Agent
from .openai_service import get_openai_response
from .grok_service import get_grok_response
import requests
from bs4 import BeautifulSoup

# --- State Management ---
# These histories will store the conversation context for each AI.
OPENAI_HISTORY = [
    {"role": "system", "content": "You are OpenAI's GPT, a helpful and direct AI assistant."}
]

GROK_HISTORY = [
    {"role": "system", "content": "You are Grok, an AI from xAI with a witty and slightly rebellious personality."}
]

# --- Tool Definition ---
def ask_multimodel_agent(prompt: str) -> str:
    """
    Routes a prompt to the appropriate AI model (OpenAI or Grok)
    and returns the response, maintaining separate conversation histories.

    To talk to Grok, start the prompt with 'grok:'. Otherwise, it defaults to OpenAI.

    Args:
        prompt (str): The user's input.

    Returns:
        str: The selected AI's response.
    """
    if prompt.lower().startswith('grok:'):
        # Select Grok
        clean_prompt = prompt[5:].strip()
        history = GROK_HISTORY
        service_func = get_grok_response
        ai_name = "Grok"
    else:
        # Default to OpenAI
        clean_prompt = prompt
        history = OPENAI_HISTORY
        service_func = get_openai_response
        ai_name = "OpenAI"

    # Add user's message to the selected AI's history
    history.append({"role": "user", "content": clean_prompt})

    # Get the response
    ai_response = service_func(history)

    # Add AI's response to its history to maintain context
    history.append({"role": "assistant", "content": ai_response})

    return f"{ai_name}: {ai_response}"


def get_website_text(url: str) -> dict:
    """
    Fetches the content of a URL and returns its visible text.

    Args:
        url (str): The URL of the website to fetch.

    Returns:
        dict: A dictionary containing the status and the extracted text or an error message.
    """
    try:
        # Add a scheme to the URL if it's missing to ensure the request works
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Set a user-agent to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Make the web request
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception if the request was not successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get the visible text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        report = '\n'.join(chunk for chunk in chunks if chunk)

        return {"status": "success", "report": report}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Network error fetching URL: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {str(e)}"}


# --- ADK Agent Definition ---
# This is the entry point for the ADK framework (`adk web`)
root_agent = Agent(
    name="giovanni_agent",
    model="gemini-2.0-flash",
    description="An agent that can route requests to different AI models like OpenAI and Grok. It can also fetch website text.",
    instruction=(
        "You are a multi-model orchestrator that can fetch website content and route requests "
        "to different AI models. When users ask about websites, use get_website_text. "
        "For general questions, answer the question directly. If the user asks for more insights, or continues to still not understand, "
        "use ask_multimodel_agent to route to the appropriate AI."
    ),
    tools=[ask_multimodel_agent, get_website_text]
)

# --- Main Chat Logic for Terminal ---
def main():
    """The main function to run the chat orchestrator in the terminal."""
    print("Giovanni's Multi-Agent Chat")
    print("Start your prompt with 'grok:' to talk to Grok. Otherwise, you'll talk to OpenAI.")
    print("Type '/bye' to exit.")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == '/bye':
                print("Goodbye!")
                break
            
            if not user_input:
                continue

            # Use the same logic as the tool for consistency
            response = ask_multimodel_agent(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# This allows the file to be run directly from the terminal
if __name__ == "__main__":
    main()
