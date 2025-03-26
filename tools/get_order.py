from fastmcp import Context
import httpx
from typing import Optional
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def get_order(
    uuid: Optional[str] = None,
    identifier: Optional[str] = None,
    ctx: Context = None
) -> dict:
    """
    업비트에서 특정 주문의 정보를 조회합니다.
    
    Args:
        uuid (str, optional): 주문 UUID
        identifier (str, optional): 조회용 사용자 지정 값
        
    Returns:
        dict: 주문 정보
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return {"error": "API 키가 설정되지 않았습니다."}
    
    if not uuid and not identifier:
        if ctx:
            ctx.error("uuid 또는 identifier 중 하나는 필수입니다.")
        return {"error": "uuid 또는 identifier 중 하나는 필수입니다."}
    
    url = f"{API_BASE}/order"
    query_params = {}
    
    if uuid:
        query_params['uuid'] = uuid
    
    if identifier:
        query_params['identifier'] = identifier
    
    headers = {
        "Authorization": f"Bearer {generate_upbit_token(query_params)}"
    }
    
    if ctx:
        ctx.info(f"주문 정보 조회 중: {uuid or identifier}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, params=query_params, headers=headers)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return {"error": f"업비트 API 오류: {res.status_code}"}
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return {"error": f"API 호출 중 오류 발생: {str(e)}"}