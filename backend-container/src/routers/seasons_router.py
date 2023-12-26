from fastapi import APIRouter
from models.seasons import SeasonInfo

router = APIRouter()

@router.get("/seasons")
async def read_seasons():
    # Logic to fetch and return seasons
    return {"seasons": "data"}
