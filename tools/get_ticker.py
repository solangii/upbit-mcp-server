import httpx
from config import API_BASE

async def get_ticker(symbol: str) -> dict:
    """Get the latest ticker data from Upbit"""
    url = f"{API_BASE}/ticker"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params={"markets": symbol})
        return res.json()[0]