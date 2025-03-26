import httpx
from fastmcp import Context
from typing import Optional
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def create_withdraw(
    currency: str,
    amount: str,
    address: Optional[str] = None,
    secondary_address: Optional[str] = None,
    transaction_type: Optional[str] = None,
    ctx: Context = None
) -> dict:
    """
    업비트에서 출금을 요청합니다.
    
    Args:
        currency (str): 통화 코드 (예: BTC)
        amount (str): 출금 수량
        address (str, optional): 출금 주소
        secondary_address (str, optional): 2차 출금 주소 (EOS, XRP 등에서 사용되는 Destination Tag, Memo)
        transaction_type (str, optional): 출금 유형
        
    Returns:
        dict: 출금 요청 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}
    
    if currency.upper() != "KRW" and not address:
        if ctx:
            ctx.error("암호화폐 출금 시 address는 필수입니다.")
        return {"error": "암호화폐 출금 시 address는 필수입니다."}
    
    # API_BASE를 사용하여 URL 구성
    url_path = "withdraws/coin" if currency.upper() != "KRW" else "withdraws/krw"
    url = f"{API_BASE}/{url_path}"
    
    query_params = {
        'currency': currency,
        'amount': amount
    }
    
    if address:
        query_params['address'] = address
    
    if secondary_address:
        query_params['secondary_address'] = secondary_address
    
    if transaction_type:
        query_params['transaction_type'] = transaction_type
    
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"{currency} 출금 요청 중: {amount}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, params=query_params, headers=headers)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return {"error": f"업비트 API 오류: {res.status_code}"}
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return {"error": f"API 호출 중 오류 발생: {str(e)}"}