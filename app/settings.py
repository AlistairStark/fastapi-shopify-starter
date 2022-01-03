import os
import sys

PROJECT_NAME = os.getenv("PROJECT_NAME", "Shopify Starter")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DBS = os.getenv("POSTGRES_DBS", "postgres")
SHOPIFY_APP_KEY = os.getenv("SHOPIFY_APP_KEY")
SHOPIFY_APP_SECRET = os.getenv("SHOPIFY_APP_SECRET")


def get_db_url():
    if "pytest" in sys.modules:
        return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PROJECT_NAME}-postgres/test"
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PROJECT_NAME}-postgres/{POSTGRES_DBS}"
