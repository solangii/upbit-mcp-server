import httpx
from fastmcp import Context
from config import generate_upbit_token, UPBIT_ACCESS_KEY, API_BASE

async def get_accounts(ctx: Context = None) -> list[dict]:
    """
    업비트 계정의 잔고 정보를 조회합니다.
    
    Returns:
        list[dict]: 보유 중인 자산 목록
    """
    if not UPBIT_ACCESS_KEY:
        if ctx:
            ctx.error("API 키가 설정되지 않았습니다. .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
        return [{"error": "API 키가 설정되지 않았습니다."}]
    
    url = f"{API_BASE}/accounts"
    headers = {
        "Authorization": f"Bearer {generate_upbit_token()}"
    }
    
    if ctx:
        ctx.info("계정 잔고 조회 중...")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return [{"error": f"업비트 API 오류: {res.status_code}"}]
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return [{"error": f"API 호출 중 오류 발생: {str(e)}"}]