import os
import sys

# choose app scopes. Comment out the ones you don't need
available_scopes = [
    # "read_all_orders",
    # "read_assigned_fulfillment_orders",
    # "write_assigned_fulfillment_orders",
    "read_checkouts",
    "write_checkouts",
    "read_content",
    "write_content",
    "read_customers",
    "write_customers",
    "read_discounts",
    "write_discounts",
    # "read_draft_orders",
    # "write_draft_orders",
    # "read_files",
    # "write_files",
    # "read_fulfillments",
    # "write_fulfillments",
    # "read_gift_cards",
    # "write_gift_cards",
    "read_inventory",
    "write_inventory",
    # "read_legal_policies",
    # "read_locales",
    # "write_locales",
    # "read_locations",
    # "read_marketing_events",
    # "write_marketing_events",
    # "read_merchant_approval_signals",
    # "read_merchant_managed_fulfillment_orders",
    # "write_merchant_managed_fulfillment_orders",
    "read_orders",
    "write_orders",
    # "read_price_rules",
    # "write_price_rules",
    "read_products",
    "write_products",
    "read_product_listings",
    # "read_publications",
    # "write_publications",
    # "read_reports",
    # "write_reports",
    # "read_resource_feedbacks",
    # "write_resource_feedbacks",
    "read_script_tags",
    "write_script_tags",
    # "read_shipping",
    # "write_shipping",
    # "read_shopify_payments_disputes",
    # "read_shopify_payments_payouts",
    # "read_themes",
    # "write_themes",
    # "read_translations",
    # "write_translations",
    # "read_third_party_fulfillment_orders",
    # "write_third_party_fulfillment_orders",
    # "read_users",
    # "write_users",
    # "write_order_edits",
]
SCOPES = ",".join(available_scopes)
PROJECT_NAME = os.getenv("PROJECT_NAME", "Shopify Starter")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DBS = os.getenv("POSTGRES_DBS", "postgres")
SHOPIFY_APP_KEY = os.getenv("SHOPIFY_APP_KEY")
SHOPIFY_APP_SECRET = os.getenv("SHOPIFY_APP_SECRET")
REDIS_URI = os.getenv("REDIS_URI")
REDIRECT_URL = (
    "https://9334-206-172-242-206.ngrok.io/v1/redirect"  # os.getenv("REDIRECT_URL")
)
SECRET = os.getenv("SECRET", "").encode()


def get_db_url():
    if "pytest" in sys.modules:
        return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PROJECT_NAME}-postgres/test"
    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PROJECT_NAME}-postgres/{POSTGRES_DBS}"


def get_redis_url():
    return REDIS_URI
