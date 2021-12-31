import os

PROJECT_NAME = os.getenv("PROJECT_NAME", "Shopify Starter")
DB_URL = os.getenv(
    "DB_URL", f"postgresql://postgres:postgres@{PROJECT_NAME}-postgres/postgres"
)
