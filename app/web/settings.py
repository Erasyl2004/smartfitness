from dotenv import load_dotenv
import os

load_dotenv()

class OtpSettings:
    gmail_user: str = os.getenv("GMAIL_USER")
    gmail_name: str = os.getenv("GMAIL_NAME")
    gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD")
    brevo_api_key: str = os.getenv("BREVO_API_KEY")