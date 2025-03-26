import httpx
from config import API_BASE

async def get_trades(symbol: str) -> list[dict]:
    """Get recent trade ticks for a symbol"""
    url = f"{API_BASE}/trades/ticks"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params={"market": symbol})
        return res.json()