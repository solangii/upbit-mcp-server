from fastmcp import Context
import httpx
from typing import Literal, Optional
from config import API_BASE

async def get_candles(
    market: str,
    interval: Literal["minute1", "minute3", "minute5", "minute10", "minute15", "minute30", "minute60", "minute240", "day", "week", "month"],
    count: int = 200,
    to: Optional[str] = None,
    ctx: Context = None
) -> list[dict]:
    """
    업비트에서 캔들스틱 데이터를 조회합니다.
    
    Args:
        market (str): 마켓 코드 (예: KRW-BTC)
        interval (str): 시간 간격 (minute1~minute240, day, week, month)
        count (int): 캔들 개수 (최대 200)
        to (str, optional): 마지막 캔들 시각 (형식: yyyy-MM-dd'T'HH:mm:ss'Z' 또는 yyyy-MM-dd HH:mm:ss)
        
    Returns:
        list[dict]: 캔들스틱 데이터
    """
    if count > 200:
        count = 200
        if ctx:
            ctx.warning("최대 200개의 캔들만 조회할 수 있습니다. count를 200으로 제한합니다.")
    
    # interval에 따라 API 엔드포인트 선택
    if interval.startswith("minute"):
        url = f"{API_BASE}/candles/{interval}"
    else:
        url = f"{API_BASE}/candles/{interval}s"
    
    params = {
        'market': market,
        'count': str(count)
    }
    
    if to:
        params['to'] = to
    
    if ctx:
        ctx.info(f"{market} {interval} 캔들 데이터 조회 중...")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, params=params)
            if res.status_code != 200:
                if ctx:
                    ctx.error(f"업비트 API 오류: {res.status_code} - {res.text}")
                return [{"error": f"업비트 API 오류: {res.status_code}"}]
            return res.json()
        except Exception as e:
            if ctx:
                ctx.error(f"API 호출 중 오류 발생: {str(e)}")
            return [{"error": f"API 호출 중 오류 발생: {str(e)}"}]