import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ira.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-jwt-key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
    VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
    VAPID_CLAIMS = {"sub": "mailto:admin@ira.app"}

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False