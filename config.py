import os
import uuid
import jwt
import hashlib
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 업비트 API 키 설정
UPBIT_ACCESS_KEY = os.environ.get("UPBIT_ACCESS_KEY")
UPBIT_SECRET_KEY = os.environ.get("UPBIT_SECRET_KEY")

# API 기본 URL
API_BASE = "https://api.upbit.com/v1"

# API 키 검증
if not UPBIT_ACCESS_KEY or not UPBIT_SECRET_KEY:
    print("경고: 업비트 API 키가 설정되지 않았습니다. 공개 API만 사용 가능합니다.")

# Upbit API 인증을 위한 JWT 토큰 생성 함수
def generate_upbit_token(query_params=None):
    """
    업비트 API 인증을 위한 JWT 토큰 생성
    
    Args:
        query_params (dict, optional): 쿼리 파라미터
        
    Returns:
        str: JWT 토큰
    """
    payload = {
        'access_key': UPBIT_ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    
    if query_params:
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        m = hashlib.sha512()
        m.update(query_string.encode())
        query_hash = m.hexdigest()
        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'
    
    return jwt.encode(payload, UPBIT_SECRET_KEY)

# 마켓 코드 유효성 검사 함수
def is_valid_market(market_code):
    """
    마켓 코드가 올바른 형식인지 검사
    
    Args:
        market_code (str): 검사할 마켓 코드
        
    Returns:
        bool: 유효한 마켓 코드인지 여부
    """
    if not market_code or not isinstance(market_code, str):
        return False
        
    # KRW, BTC, USDT 마켓 형식 확인
    parts = market_code.split('-')
    if len(parts) != 2:
        return False
        
    market_type, ticker = parts
    if market_type not in ['KRW', 'BTC', 'USDT']:
        return False
        
    return True

# 주문 유형 유효성 검사 함수
def validate_order_params(market, side, ord_type, volume=None, price=None):
    """
    주문 파라미터 유효성 검사
    
    Args:
        market (str): 마켓 코드
        side (str): 주문 종류 (bid/ask)
        ord_type (str): 주문 타입 (limit/price/market)
        volume (str, optional): 주문량
        price (str, optional): 주문 가격
        
    Returns:
        tuple: (유효성 여부, 오류 메시지)
    """
    if not is_valid_market(market):
        return False, "유효하지 않은 마켓 코드입니다."
        
    if side not in ['bid', 'ask']:
        return False, "side는 'bid' 또는 'ask'여야 합니다."
        
    if ord_type not in ['limit', 'price', 'market']:
        return False, "ord_type은 'limit', 'price', 'market' 중 하나여야 합니다."
        
    if ord_type == 'limit' and (not volume or not price):
        return False, "지정가 주문에는 volume과 price가 모두 필요합니다."
        
    if ord_type == 'price' and not price:
        return False, "시장가 매수 주문에는 price가 필요합니다."
        
    if ord_type == 'market' and not volume:
        return False, "시장가 매도 주문에는 volume이 필요합니다."
        
    return True, ""

# 시간 간격 형식 유효성 검사
def is_valid_interval(interval):
    """
    캔들 시간 간격의 유효성 검사
    
    Args:
        interval (str): 시간 간격
        
    Returns:
        bool: 유효한 시간 간격인지 여부
    """
    valid_minutes = [f"minute{i}" for i in [1, 3, 5, 10, 15, 30, 60, 240]]
    valid_others = ["day", "week", "month"]
    
    return interval in valid_minutes + valid_others

# 에러 응답 생성 함수
def create_error_response(message, status_code=400):
    """
    에러 응답 생성
    
    Args:
        message (str): 에러 메시지
        status_code (int): HTTP 상태 코드
        
    Returns:
        dict: 에러 응답
    """
    return {
        "error": {
            "message": message,
            "status": status_code
        }
    }

# 주요 암호화폐 목록 (기술적 분석 등에 사용)
MAJOR_COINS = [
    "KRW-BTC",  # 비트코인
    "KRW-ETH",  # 이더리움
    "KRW-XRP",  # 리플
    "KRW-SOL",  # 솔라나
    "KRW-ADA",  # 에이다
    "KRW-DOGE", # 도지코인
    "KRW-AVAX", # 아발란체
    "KRW-DOT",  # 폴카닷
    "KRW-MATIC" # 폴리곤
]