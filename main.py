# main.py
from fastmcp import FastMCP
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, API_BASE
import httpx

from tools.get_ticker import get_ticker
from tools.get_orderbook import get_orderbook
from tools.get_trades import get_trades
from tools.get_accounts import get_accounts
from tools.create_order import create_order
from tools.get_orders import get_orders
from tools.get_order import get_order
from tools.cancel_order import cancel_order
from tools.get_market_summary import get_market_summary
from tools.get_deposits_withdrawals import get_deposits_withdrawals

from prompts.explain_ticker import explain_ticker
from prompts.analyze_portfolio import analyze_portfolio
from prompts.order_help import order_help
from prompts.trading_strategy import trading_strategy

from resources.get_market_list import get_market_list


if not UPBIT_ACCESS_KEY or not UPBIT_SECRET_KEY:
    print("⚠️  경고: 업비트 API 키가 설정되지 않았습니다. 공개 API만 사용 가능합니다.")
    print("     .env 파일에 UPBIT_ACCESS_KEY와 UPBIT_SECRET_KEY를 설정해주세요.")
else:
    print("✅ 업비트 API 키가 확인되었습니다. 모든 기능을 사용할 수 있습니다.")

mcp = FastMCP(
    "Upbit MCP Server", 
    description="Upbit 암호화폐 거래소 API와 연동된 MCP 서버",
    dependencies=[
        "httpx>=0.27.0",
        "pyjwt",
        "python-dotenv",
        "numpy"
    ]
)

mcp.tool()(get_ticker)
mcp.tool()(get_orderbook)
mcp.tool()(get_trades)
mcp.tool()(get_accounts)
mcp.tool()(create_order)
mcp.tool()(get_orders)
mcp.tool()(get_order)
mcp.tool()(cancel_order)
mcp.tool()(get_market_summary)
mcp.tool()(get_deposits_withdrawals)

mcp.resource("market://list")(get_market_list)

mcp.prompt()(explain_ticker)
mcp.prompt()(analyze_portfolio)
mcp.prompt()(order_help)
mcp.prompt()(trading_strategy)

if __name__ == "__main__":
    print("업비트 MCP 서버가 시작되었습니다!")
    mcp.run(transport="stdio")  # Claude, gomcp 연동용