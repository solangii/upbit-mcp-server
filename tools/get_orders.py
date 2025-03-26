from fastmcp import Context
import httpx
from typing import Optional, Literal
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def get_orders(
    market: Optional[str] = None,
    state: Literal["wait", "done", "cancel"] = "wait",
    page: int = 1,
    limit: int = 100,
    ctx: Context = None
) -> list[dict]:
    """
    업비트에서 주문 내역을 조회합니다.
    
    Args:
        market (str, optional): 마켓 코드 (예: KRW-BTC)
        state (str): 주문 상태 - wait(대기), done(완료), cancel(취소)
        page (int): 페이지 번호
        limit (int): 페이지당 주문 개수 (최대 100)
        
    Returns:
        list[dict]: 주문 내역
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]
    
    url = f"{API_BASE}/orders"
    query_params = {
        'state': state,
        'page': str(page),
        'limit': str(limit)
    }
    
    if market:
        query_params['market'] = market
    
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"주문 내역 조회 중: 상태={state}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, params=query_params, headers=headers)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return [{"error": f"업비트 API 오류: {res.status_code}"}]
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return [{"error": f"API 호출 중 오류 발생: {str(e)}"}]