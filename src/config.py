import os

from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT"))
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_MAIL = os.getenv("RECIPIENT_MAIL")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

RESEARCH_PROFILE = os.getenv("RESEARCH_PROFILE")
