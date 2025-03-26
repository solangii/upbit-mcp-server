import httpx
from config import API_BASE

async def get_orderbook(symbol: str) -> dict:
    """Get orderbook snapshot for a given symbol"""
    url = f"{API_BASE}/orderbook"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params={"markets": symbol})
        return res.json()[0]