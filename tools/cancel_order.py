import httpx
from fastmcp import Context
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def cancel_order(
    uuid: str,
    ctx: Context = None
) -> dict:
    """
    업비트에서 주문을 취소합니다.
    
    Args:
        uuid (str): 취소할 주문의 UUID
        
    Returns:
        dict: 취소 결과
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}
    
    url = f"{API_BASE}/order"
    query_params = {'uuid': uuid}
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"주문 취소 중: {uuid}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.delete(url, params=query_params, headers=headers)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return {"error": f"업비트 API 오류: {res.status_code}"}
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return {"error": f"API 호출 중 오류 발생: {str(e)}"}