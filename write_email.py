"""
This file is dedicated to writing emails to professors using generative AI.
To successfully write an email, the program needs to
    1. Retrieve the professor's information from the database.
    2. Find the professor's Google Scholar profile.
        - Use genAI to find the link for the professor's Google Scholar profile.
    3. Read the professor's publications, recent and popular.
        - Scrap the profile to get the publications, and ask the user to select the most relevant one to base the email on.
    4. Use the information to write a personalized email along with examples from previous emails sent (retrueived from the database).


"""

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def findGoogleScholar():
    """
    This function is intended to find Google Scholar profiles.
    Currently, it does not implement any functionality.
    """
    pass