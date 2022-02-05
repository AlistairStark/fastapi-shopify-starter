import logging
from typing import Optional
from fastapi import HTTPException
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode
from app.models.shop import Shop
from app import settings

from app.services.verification import Verification


logger = logging.getLogger(__name__)


class ShopifyApi:
    def __init__(
        self,
        shop: Shop,
        verification_service: Verification = Verification(),
    ) -> None:
        self.shop = shop
        self.verification_service = verification_service
        token = self.verification_service.decrypt(shop.token)
        headers = {
            "X-Shopify-Access-Token": token,
        }
        url = f"https://{self.shop.shop_name}.myshopify.com/admin/api/2022-01/graphql.json"
        transport = AIOHTTPTransport(headers=headers, url=url)
        self.client = Client(transport=transport)

    async def _make_request(
        self,
        query: DocumentNode,
        variables: Optional[dict] = None,
    ):
        async with self.client as session:
            try:
                result = await session.execute(query, variable_values=variables)
                if not isinstance(result, dict):
                    return {}
                return result
            except Exception as e:
                logger.error(e)
                raise HTTPException(
                    502, detail="There was an error communicating with Shopify"
                )

    async def get_products(self):
        """Gets a permanent access token for a store"""
        query = gql(
            """
                query {
                    products (first: 3) {
                        edges {
                            node {
                                id
                                title
                            }
                        }
                    }
                }
            """
        )
        return await self._make_request(query)

    async def is_dev_store(self) -> bool:
        """Check if a store is subscribed or a dev store"""
        query = gql(
            """
                query {
                    shop {
                        plan {
                            partnerDevelopment
                        }
                    }
                }
            """
        )
        data = await self._make_request(query)
        return data.get("shop", {}).get("plan", {}).get("partnerDevelopment", False)

    async def create_subscription(self, nonce: str) -> str:
        """Creates a subscription with a trial period for a store. Returns the merchant redirect URL to confirm the subscription"""
        mutation = gql(
            """
            mutation appSubscriptionCreate(
                $lineItems: [AppSubscriptionLineItemInput!]!, 
                $name: String!, 
                $returnUrl: URL!,
                $test: Boolean!,
                $trialDays: Int!
            ) {
                appSubscriptionCreate(
                    lineItems: $lineItems, 
                    name: $name, 
                    returnUrl: $returnUrl,
                    test: $test,
                    trialDays: $trialDays
                ) {
                    confirmationUrl
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
        )
        variables = {
            "lineItems": {
                "plan": {
                    "appRecurringPricingDetails": {
                        "interval": "EVERY_30_DAYS",
                        "price": {"amount": "9.99", "currencyCode": "USD"},
                    },
                }
            },
            "name": "Monthly Subscription",
            "returnUrl": f"{settings.BASE_URL}/api/v1/sub?shop_name={self.shop.shop_name}&nonce={nonce}",
            # TODO should not be test for prod!
            "test": True,
            "trialDays": 7,
        }
        data = await self._make_request(mutation, variables)
        return data.get("appSubscriptionCreate", {}).get("confirmationUrl")
