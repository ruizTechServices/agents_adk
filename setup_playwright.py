import subprocess
import sys

def install():
    try:
        print("Installing Playwright library...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        print("Playwright library installed.")
        
        print("Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("Playwright browsers installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install()
