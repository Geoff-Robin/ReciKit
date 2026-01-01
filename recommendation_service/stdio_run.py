from recommendation.app import mcp_app
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    mcp_app.run()