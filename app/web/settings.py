from dotenv import load_dotenv
import os

load_dotenv()

class OtpSettings:
    gmail_user: str = os.getenv("GMAIL_USER")
    gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD")