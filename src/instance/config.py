import os

# General
DEBUG = os.getenv("DEBUG", "True").strip().lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-placeholder-key")

# Raise error if key is insecure in production
if not DEBUG and SECRET_KEY == "dev-placeholder-key":
    raise RuntimeError("SECURITY RISK: Please set a secure SECRET_KEY in production.")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Push Notifications (VAPID for web push)
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
VAPID_SUB = os.getenv("VAPID_SUB", "mailto:admin@example.com")
VAPID_CLAIMS = {
    "sub": VAPID_SUB
}

# App logic thresholds
try:
    MIN_HYDRATION_L = float(os.getenv("MIN_HYDRATION_L", "1.5"))
    MIN_SLEEP_HOURS = float(os.getenv("MIN_SLEEP_HOURS", "6.0"))
except ValueError:
    raise ValueError("Environment variables MIN_HYDRATION_L and MIN_SLEEP_HOURS must be valid floats.")