from app.models.shop import Shop


async def create_shop(params: dict, db_session):
    async with db_session as session:
        s = Shop(**params)
        session.add(s)
        await session.commit()
