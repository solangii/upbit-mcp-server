def analyze_portfolio(account_data: list[dict]) -> str:
    """
    사용자의 포트폴리오를 분석하는 프롬프트를 생성합니다.
    """
    portfolio_summary = ""
    total_krw = 0
    
    for asset in account_data:
        if asset['currency'] == 'KRW':
            total_krw = float(asset['balance'])
        else:
            asset_value = float(asset['balance']) * (float(asset.get('avg_buy_price', 0)) or 0)
            portfolio_summary += f"- {asset['currency']}: {asset['balance']} 개 보유 (평균 매수가: {asset.get('avg_buy_price', '정보 없음')} KRW)\n"
    
    return f"""
    🏦 업비트 포트폴리오 분석
    
    현재 KRW 잔액: {total_krw:,.0f} 원
    
    보유 자산:
    {portfolio_summary}
    
    위 포트폴리오에 대해 분석해주세요. 각 자산의 비중과 현재 시장 상황을 고려하여 조언을 제공해주세요.
    필요하다면 get_ticker 도구를 통해 현재 가격 정보를 확인할 수 있습니다.
    """