# Upbit MCP Server

A server implementation for [Upbit](https://upbit.com) Cryptocurrency Exchange OpenAPI using the Model Context Protocol (MCP). This project provides tools to interact with Upbit exchange services, such as retrieving market data (quotes, orderbooks, trade history, chart data), account information, creating and canceling orders, managing deposits/withdrawals, and performing technical analysis.

## Features

- Market data retrieval (ticker, orderbook, trades, candle data)
- Account information (balance, order history)
- Order creation and cancellation
- Deposit and withdrawal functions
- Technical analysis tools

## Prerequisites

Before you begin, you need to get your Upbit API keys:

1. Create an account on [Upbit](https://upbit.com) if you don't already have one
2. Go to the [Upbit Developer Center](https://upbit.com/service_center/open_api_guide)
3. Create a new API key
4. Make sure to set appropriate permissions (read, trade, withdraw as needed)
5. Store your API keys(`UPBIT_ACCESS_KEY`, `UPBIT_SECRET_KEY`) in the `.env` file (see Installation section)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/upbit-mcp-server.git
   cd upbit-mcp-server
   ```

2. Install dependencies:
   ```bash
   # Using pip
   pip install -e .
   
   # Or using uv (recommended)
   uv pip install -e .
   ```

   Using uv provides faster installation and more reliable dependency resolution. To install uv:
   ```bash
   # Install uv
   curl -fsSL https://install.ultramarine.tools | sh
   
   # Or install with pip
   pip install uv
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add your Upbit API keys:
   ```
   UPBIT_ACCESS_KEY=your_access_key_here
   UPBIT_SECRET_KEY=your_secret_key_here
   ```

## Usage

### Development Mode (Web Interface)

```bash
fastmcp dev main.py
```

### Install in Claude Desktop

```bash
fastmcp install main.py --name "Upbit API"
```

### Run Directly with Python

```bash
python main.py

# Or using uv
uv run python main.py
```

## Caution

- This server can process real trades, so use it carefully.
- Keep your API keys secure and never commit them to public repositories.
- Thoroughly test before using in production environments.

## License

MIT
