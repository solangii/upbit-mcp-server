import httpx
from config import API_BASE

async def get_market_list() -> list[str]:
    """Get available trading pairs from Upbit"""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_BASE}/market/all")
        return [item["market"] for item in res.json()]