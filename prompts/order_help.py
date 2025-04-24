def order_help() -> str:
    """
    주문 생성에 대한 도움말 프롬프트를 생성합니다.
    """
    return """
    업비트 주문 생성 가이드
    
    주문을 생성하기 위해 다음 정보가 필요합니다:
    
    1. 마켓 코드 (예: KRW-BTC, KRW-ETH)
    2. 주문 종류
       - bid: 매수
       - ask: 매도
    3. 주문 타입
       - limit: 지정가 주문 (volume과 price 모두 필요)
       - price: 시장가 매수 (price만 필요, 주문 총액)
       - market: 시장가 매도 (volume만 필요, 주문 수량)
    4. volume: 주문량 (지정가 및 시장가 매도 필수)
    5. price: 주문 가격 (지정가 및 시장가 매수 필수)
    
    주문 예시:
    1. 비트코인 100,000원어치 시장가 매수:
       create_order(market="KRW-BTC", side="bid", ord_type="price", price="100000")
    
    2. 이더리움 0.1개 시장가 매도:
       create_order(market="KRW-ETH", side="ask", ord_type="market", volume="0.1")
    
    3. 리플 500개 1,000원에 지정가 매수:
       create_order(market="KRW-XRP", side="bid", ord_type="limit", volume="500", price="1000")
    
    주의사항:
    - 주문 전에 get_accounts 도구로 보유 잔고를 확인하세요.
    - 주문 후에는 get_orders 도구로 주문 상태를 확인할 수 있습니다.
    - 취소하려면 cancel_order 도구를 사용하세요.
    """