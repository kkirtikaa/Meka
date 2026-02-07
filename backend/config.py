import os
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()

class Config:
    # -----------------------------
    # Flask / Security
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # -----------------------------
    # MongoDB
    # -----------------------------
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/meka_db"
    )

    # -----------------------------
    # Cloudinary
    # -----------------------------
    CLOUD_NAME = os.getenv("CLOUD_NAME")
    CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
    CLOUD_API_SECRET = os.getenv("CLOUD_API_SECRET")