cd app && alembic upgrade head && cd ..

uvicorn app:app --reload --host 0.0.0.0