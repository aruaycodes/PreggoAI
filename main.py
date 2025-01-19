
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

# Initialize OpenAI with the API key
openai.api_key = openai_api_key
