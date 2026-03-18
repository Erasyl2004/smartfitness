from dotenv import load_dotenv
import os

load_dotenv()

class OtpSettings:
    gmail_user: str = os.getenv("GMAIL_USER")
    gmail_name: str = os.getenv("GMAIL_NAME")
    gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD")
    brevo_api_key: str = os.getenv("BREVO_API_KEY")

class AiSettings:
    api_key: str = os.getenv("AI_API_KEY")
    gpt_model: str = "gemini-2.5-flash"
    temperature: float = 0

class S3Settings:
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name: str = os.getenv("AWS_REGION_NAME")
    bucket_name: str = os.getenv("AWS_BUCKET_NAME")