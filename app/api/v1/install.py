from fastapi import APIRouter

router = APIRouter()


@router.get("/install")
def install_app():
    return {"message": "hi there"}


@router.get("/redirect")
def install_app():
    return {"message": "hi there"}
