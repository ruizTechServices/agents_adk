import requests
from bs4 import BeautifulSoup
from google.adk.agents import Agent
from .openai_service import get_openai_response

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


def ask_openai_agent(question: str) -> dict:
    """
    Ask the OpenAI agent a question and return the response.
    
    Args:
        question (str): The question to ask the OpenAI agent.
    
    Returns:
        dict: A dictionary containing the status and the response from the OpenAI agent or an error message.
    """
    try:
        response = get_openai_response(question)
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {str(e)}"}


root_agent = Agent(
    name="giovanni_agent",
    model="gemini-1.5-flash",
    description="An agent for Giovanni that can fetch and read the text content of web pages.",
    instruction="You are a helpful agent for Giovanni. Use the get_website_text tool to retrieve the textual content from a URL.",
    tools=[get_website_text, ask_openai_agent],
)