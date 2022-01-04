import pytest

from app.services.nonce_service import NonceService


@pytest.mark.asyncio
async def test_nonce_service_create():
    shop_name = "testshop"
    nonce_service = NonceService()
    nonce = await nonce_service.create(shop_name)
    got = await nonce_service.get(shop_name)
    is_valid = await nonce_service.validate(shop_name, nonce)

    assert is_valid
    assert got == nonce

    await nonce_service.delete(shop_name)


@pytest.mark.asyncio
async def test_nonce_service_create_no_nonce():
    shop_name = "testshoprandom"
    nonce_service = NonceService()
    nonce = "arandomstring"
    got = await nonce_service.get(shop_name)
    is_valid = await nonce_service.validate(shop_name, nonce)

    assert is_valid is False
    assert got == None

    await nonce_service.delete(shop_name)


@pytest.mark.asyncio
async def test_nonce_service_delete_nonce():
    shop_name = "testshop"
    nonce_service = NonceService()
    nonce = await nonce_service.create(shop_name)
    await nonce_service.delete(shop_name)
    got = await nonce_service.get(shop_name)
    assert nonce is not None
    assert got == None
