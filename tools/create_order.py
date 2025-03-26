import httpx
from fastmcp import Context
from typing import Literal, Optional
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def create_order(
    market: str, 
    side: Literal["bid", "ask"], 
    ord_type: Literal["limit", "price", "market"],
    volume: Optional[str] = None,
    price: Optional[str] = None,
    ctx: Context = None
) -> dict:
    """
    업비트에 주문을 생성합니다.
    
    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        side (str): 주문 종류 - bid(매수) 또는 ask(매도)
        ord_type (str): 주문 타입 - limit(지정가), price(시장가 매수), market(시장가 매도)
        volume (str, optional): 주문량 (지정가, 시장가 매도 필수)
        price (str, optional): 주문 가격 (지정가 필수, 시장가 매수 필수)
        
    Returns:
        dict: 주문 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}
    
    # 주문 유효성 검사
    if ord_type == "limit" and (not volume or not price):
        if ctx:
            ctx.error("지정가 주문에는 volume과 price가 모두 필요합니다.")
        return {"error": "지정가 주문에는 volume과 price가 모두 필요합니다."}
    
    if ord_type == "price" and not price:
        if ctx:
            ctx.error("시장가 매수 주문에는 price가 필요합니다.")
        return {"error": "시장가 매수 주문에는 price가 필요합니다."}
    
    if ord_type == "market" and not volume:
        if ctx:
            ctx.error("시장가 매도 주문에는 volume이 필요합니다.")
        return {"error": "시장가 매도 주문에는 volume이 필요합니다."}
    
    url = f"{API_BASE}/orders"
    query_params = {
        'market': market,
        'side': side,
        'ord_type': ord_type
    }
    
    if volume:
        query_params['volume'] = volume
    
    if price:
        query_params['price'] = price
    
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"주문 생성 중: {market} {side} {ord_type}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, params=query_params, headers=headers)
            if res.status_code != 201:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return {"error": f"업비트 API 오류: {res.status_code}"}
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return {"error": f"API 호출 중 오류 발생: {str(e)}"}