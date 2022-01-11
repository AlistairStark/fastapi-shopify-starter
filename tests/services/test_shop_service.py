import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.services.shop_service import ShopService


@pytest.mark.asyncio
async def test_create_shop(db_session: AsyncSession):
    shop_service = ShopService(db_session)
    await shop_service.create_shop("test", "123", "testscope")
    shop = await shop_service.get_shop("test")

    assert shop

    got = {
        "shop_name": shop.shop_name,
        "scopes": shop.scopes,
    }

    expected = {
        "shop_name": "test",
        "scopes": "testscope",
    }

    assert got == expected
