import yfinance as yf
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def get_stock_price(stock_code: str) -> Optional[float]:
    """
    Get current stock price from Yahoo Finance.
    Indonesian stocks use .JK suffix (Jakarta Stock Exchange).
    
    Args:
        stock_code: Stock ticker code (e.g., 'BBCA', 'TLKM')
        
    Returns:
        Current stock price or None if not found
    """
    try:
        # Add .JK suffix for Indonesian stocks
        ticker_symbol = f"{stock_code}.JK"
        
        # Fetch stock data
        stock = yf.Ticker(ticker_symbol)
        
        # Get current price from info
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if current_price:
            return float(current_price)
        
        # Fallback: try to get from history
        hist = stock.history(period='1d')
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        
        return None
        
    except Exception as e:
        print(f"Error fetching price for {stock_code}: {e}")
        return None


def get_multiple_stock_prices(stock_codes: List[str], max_workers: int = 10) -> Dict[str, Optional[float]]:
    """
    Get current prices for multiple stocks concurrently.
    
    Args:
        stock_codes: List of stock ticker codes
        max_workers: Maximum number of concurrent requests
        
    Returns:
        Dictionary mapping stock codes to their current prices
    """
    prices = {}
    
    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_stock = {
            executor.submit(get_stock_price, code): code 
            for code in stock_codes
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_stock):
            stock_code = future_to_stock[future]
            try:
                price = future.result()
                prices[stock_code] = price
            except Exception as e:
                print(f"Error processing {stock_code}: {e}")
                prices[stock_code] = None
    
    return prices


def enrich_stocks_with_prices(stocks: List[Dict]) -> List[Dict]:
    """
    Enrich stock data with current prices from Yahoo Finance.
    Also recalculates diff_pct based on current price.
    
    Args:
        stocks: List of stock dictionaries
        
    Returns:
        Updated stocks list with current_price and diff_pct fields populated
    """
    # Extract unique stock codes
    stock_codes = list(set(stock['stock_code'] for stock in stocks))
    
    print(f"Fetching prices for {len(stock_codes)} stocks...")
    
    # Fetch all prices concurrently
    prices = get_multiple_stock_prices(stock_codes)
    
    # Update stocks with prices and recalculate diff_pct
    for stock in stocks:
        code = stock['stock_code']
        current_price = prices.get(code)
        stock['current_price'] = current_price
        
        # Recalculate diff_pct based on current price vs broker average
        if current_price:
            # Determine broker's average price (buy or sell, whichever is non-zero)
            broker_avg = stock.get('buy_avg_price', 0) or stock.get('sell_avg_price', 0)
            
            if broker_avg > 0:
                # diff_pct = ((current_price - broker_avg) / broker_avg) * 100
                stock['diff_pct'] = round(((current_price - broker_avg) / broker_avg) * 100, 2)
            else:
                stock['diff_pct'] = 0.0
        # If no current price, keep original diff_pct (buy vs sell spread)
    
    # Count successful fetches
    successful = sum(1 for p in prices.values() if p is not None)
    print(f"Successfully fetched {successful}/{len(stock_codes)} prices")
    
    return stocks


def calculate_unrealized_pnl(stock: Dict) -> Optional[float]:
    """
    Calculate unrealized P&L based on current price vs average price.
    
    Args:
        stock: Stock dictionary with current_price and position data
        
    Returns:
        Unrealized P&L amount or None if current_price not available
    """
    current_price = stock.get('current_price')
    if not current_price:
        return None
    
    # Calculate based on net position
    net_lot = stock.get('net_lot', 0)
    buy_avg_price = stock.get('buy_avg_price', 0)
    
    if net_lot > 0:  # NET BUY position
        # Unrealized P&L = (Current Price - Buy Avg Price) * Net Lot * 100
        unrealized_pnl = (current_price - buy_avg_price) * net_lot * 100
        return unrealized_pnl
    elif net_lot < 0:  # NET SELL position
        # For short positions (if applicable)
        sell_avg_price = stock.get('sell_avg_price', 0)
        unrealized_pnl = (sell_avg_price - current_price) * abs(net_lot) * 100
        return unrealized_pnl
    
    return 0.0
