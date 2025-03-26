from fastmcp import Context
import httpx
from config import API_BASE, MAJOR_COINS, create_error_response

async def get_market_summary(ctx: Context = None) -> dict:
    """
    주요 암호화폐 시장의 요약 정보를 제공합니다.
    
    Returns:
        dict: 주요 암호화폐 시장 요약 정보
    """
    async with httpx.AsyncClient() as client:
        # 마켓 정보 가져오기
        markets_res = await client.get(f"{API_BASE}/market/all")
        if markets_res.status_code != 200:
            if ctx:
                ctx.error(f"마켓 정보 조회 실패: {markets_res.status_code}")
            return create_error_response("마켓 정보 조회에 실패했습니다.", markets_res.status_code)
        
        all_markets = markets_res.json()
        krw_markets = [market for market in all_markets if market["market"].startswith("KRW-")]
        
        # 티커 정보 가져오기 (50개씩 나누어 요청)
        all_tickers = []
        chunk_size = 50
        
        for i in range(0, len(krw_markets), chunk_size):
            chunk = krw_markets[i:i+chunk_size]
            markets_param = ",".join([market["market"] for market in chunk])
            
            ticker_res = await client.get(f"{API_BASE}/ticker", params={"markets": markets_param})
            if ticker_res.status_code != 200:
                if ctx:
                    ctx.warning(f"일부 티커 정보 조회 실패: {ticker_res.status_code}")
                continue
                
            all_tickers.extend(ticker_res.json())
        
        # 주요 코인 정보
        major_coin_info = [ticker for ticker in all_tickers if ticker["market"] in MAJOR_COINS]
        
        # 상위 거래량 코인 (주요 코인 제외)
        volume_sorted = sorted([t for t in all_tickers if t["market"] not in MAJOR_COINS], 
                              key=lambda x: x["acc_trade_price_24h"], 
                              reverse=True)
        top_volume_coins = volume_sorted[:5]
        
        # 상위 상승률 코인
        price_change_sorted = sorted(all_tickers, key=lambda x: x["signed_change_rate"], reverse=True)
        top_gainers = price_change_sorted[:5]
        
        # 상위 하락률 코인
        top_losers = price_change_sorted[-5:]
        
        return {
            "timestamp": all_tickers[0]["timestamp"] if all_tickers else None,
            "major_coins": major_coin_info,
            "top_volume": top_volume_coins,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "krw_market_count": len(krw_markets)
        }