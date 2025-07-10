from playwright.sync_api import sync_playwright, Page, Browser
from google.adk.agents import Agent

# Global state for the browser and page
browser: Browser = None
page: Page = None

def navigate(url: str) -> dict:
    """Navigates to a URL in a browser. Initializes the browser if not already running."""
    global browser, page
    try:
        if browser is None or not browser.is_connected():
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='domcontentloaded')
        return {"status": "success", "report": f"Successfully navigated to {url}"}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def click(selector: str) -> dict:
    """Clicks on an element specified by a CSS selector."""
    if page is None:
        return {"status": "error", "error_message": "Browser not initialized. Please navigate to a URL first."}
    try:
        page.click(selector)
        return {"status": "success", "report": f"Clicked on element '{selector}'"}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_page_content() -> dict:
    """Returns the full HTML content of the current page."""
    if page is None:
        return {"status": "error", "error_message": "Browser not initialized. Please navigate to a URL first."}
    try:
        content = page.content()
        return {"status": "success", "report": content}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def close_browser() -> dict:
    """Closes the browser session."""
    global browser, page
    if browser and browser.is_connected():
        browser.close()
        browser = None
        page = None
        return {"status": "success", "report": "Browser closed successfully."}
    return {"status": "success", "report": "Browser was not running."}

root_agent = Agent(
    name="giovanni_agent",
    model="gemini-1.5-flash",
    description="An agent for Giovanni that can interactively browse the web.",
    instruction="You are a helpful agent for Giovanni. Use the browser tools to navigate, click, and read web pages.",
    tools=[navigate, click, get_page_content, close_browser],
)