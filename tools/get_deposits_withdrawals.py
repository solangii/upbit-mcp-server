from fastmcp import Context
import httpx
from typing import Literal, Optional
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def get_deposits_withdrawals(
    currency: Optional[str] = None,
    txid: Optional[str] = None,
    transaction_type: Literal["deposit", "withdraw"] = "deposit",
    page: int = 1,
    limit: int = 100,
    ctx: Context = None
) -> list[dict]:
    """
    업비트 계정의 입출금 내역을 조회합니다.
    
    Args:
        currency (str, optional): 통화 코드 (예: BTC)
        txid (str, optional): 거래 ID
        transaction_type (str): 거래 유형 - deposit(입금) 또는 withdraw(출금)
        page (int): 페이지 번호
        limit (int): 페이지당 결과 개수 (최대 100)
        
    Returns:
        list[dict]: 입출금 내역
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]
    
    url = f"{API_BASE}/{transaction_type}s"
    query_params = {
        'page': str(page),
        'limit': str(limit)
    }
    
    if currency:
        query_params['currency'] = currency
    
    if txid:
        query_params['txid'] = txid
    
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"{transaction_type} 내역 조회 중")
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