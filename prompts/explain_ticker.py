def explain_ticker(ticker_data: dict) -> str:
    """Create a prompt explaining ticker data"""
    return f"""
    🪙 시세 요약:
    마켓: {ticker_data['market']}
    현재가: {ticker_data['trade_price']} KRW
    고가: {ticker_data['high_price']} / 저가: {ticker_data['low_price']}
    변동률: {ticker_data['signed_change_rate'] * 100:.2f}%
    """