from typing import List, Dict, Any, Optional
import json
from datetime import datetime


def parse_xhr_response(json_data: Any) -> Dict[str, Any]:
    """
    Parse XHR intercepted response data for broker summary.
    Returns array of broker summaries (one per XHR entry).
    
    Args:
        json_data: Can be a single object or array of objects from XHR interception
        
    Returns:
        Array of processed broker summary data
    """
    
    # Ensure we're working with a list
    if isinstance(json_data, dict):
        entries = [json_data]
    elif isinstance(json_data, list):
        entries = json_data
    else:
        raise ValueError("Invalid data format. Expected object or array.")
    
    if not entries:
        raise ValueError("No data entries found.")
    
    # Process each entry separately (each becomes a separate table)
    broker_summaries = []
    
    for entry in entries:
        broker_summary = process_single_entry(entry)
        if broker_summary:
            broker_summaries.append(broker_summary)
    
    return {
        'broker_summaries': broker_summaries,
        'total_entries': len(broker_summaries)
    }


def process_single_entry(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process a single XHR entry into a broker summary."""
    try:
        # Extract broker info
        broker_code = entry.get('broker', 'Unknown')
        periode = entry.get('periode', {})
        
        # Extract response data
        response_data = entry.get('response', {}).get('data', {})
        
        # Get broker name from response data (more accurate)
        broker_name = response_data.get('broker_name', get_broker_name(broker_code))
        
        broker_info = {
            'broker_code': broker_code,
            'broker_name': broker_name,
            'date_start': periode.get('from', ''),
            'date_end': periode.get('to', ''),
            'timestamp': entry.get('timestamp', ''),
            'source': entry.get('source', 'XHR')
        }
        
        broker_summary = response_data.get('broker_summary', {})
        
        # Process buy and sell transactions
        stocks = []
        
        # Process buy transactions
        brokers_buy = broker_summary.get('brokers_buy', [])
        for buy_item in brokers_buy:
            stock = process_buy_transaction(buy_item)
            if stock:
                stocks.append(stock)
        
        # Process sell transactions
        brokers_sell = broker_summary.get('brokers_sell', [])
        for sell_item in brokers_sell:
            stock = process_sell_transaction(sell_item)
            if stock:
                stocks.append(stock)
        
        # Merge stocks with same code
        merged_stocks = merge_stock_data(stocks)
        
        # Sort by absolute value (highest first)
        sorted_stocks = sorted(
            merged_stocks, 
            key=lambda x: abs(x.get('value_raw', 0)), 
            reverse=True
        )
        
        # Enrich with current prices from Yahoo Finance
        try:
            from api.service_stock.broker_summary.stock_price import enrich_stocks_with_prices
            sorted_stocks = enrich_stocks_with_prices(sorted_stocks)
        except Exception as e:
            print(f"Warning: Could not fetch stock prices: {e}")
            # Continue without prices if fetch fails
        
        # Calculate summary statistics
        total_buy_value = sum(s['buy_value'] for s in sorted_stocks)
        total_sell_value = sum(s['sell_value'] for s in sorted_stocks)
        net_value = total_buy_value - total_sell_value
        
        return {
            'broker_info': broker_info,
            'stocks': sorted_stocks,
            'total_stocks': len(sorted_stocks),
            'summary': {
                'total_buy_value': total_buy_value,
                'total_sell_value': total_sell_value,
                'net_value': net_value,
                'total_buy_value_formatted': format_currency(total_buy_value),
                'total_sell_value_formatted': format_currency(total_sell_value),
                'net_value_formatted': format_currency(abs(net_value)),
                'position': 'NET BUY' if net_value > 0 else 'NET SELL' if net_value < 0 else 'NEUTRAL'
            }
        }
    except Exception as e:
        print(f"Error processing entry: {e}")
        return None


def process_buy_transaction(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process a buy transaction item."""
    try:
        stock_code = item.get('netbs_stock_code', '')
        lot = parse_number(item.get('blot', '0'))
        value = parse_number(item.get('bval', '0'))
        avg_price = parse_number(item.get('netbs_buy_avg_price', '0'))
        
        return {
            'stock_code': stock_code,
            'transaction_type': 'BUY',
            'lot': lot,
            'value_raw': value,
            'avg_price': avg_price,
            'investor_type': item.get('type', 'Unknown')
        }
    except Exception as e:
        print(f"Error processing buy transaction: {e}")
        return None


def process_sell_transaction(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process a sell transaction item."""
    try:
        stock_code = item.get('netbs_stock_code', '')
        lot = parse_number(item.get('slot', '0'))
        value = parse_number(item.get('sval', '0'))
        avg_price = parse_number(item.get('netbs_sell_avg_price', '0'))
        
        return {
            'stock_code': stock_code,
            'transaction_type': 'SELL',
            'lot': lot,
            'value_raw': value,
            'avg_price': avg_price,
            'investor_type': item.get('type', 'Unknown')
        }
    except Exception as e:
        print(f"Error processing sell transaction: {e}")
        return None


def merge_stock_data(stocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge buy and sell transactions for the same stock.
    Calculate net position and percentage change.
    """
    stock_map = {}
    
    for stock in stocks:
        code = stock['stock_code']
        
        if code not in stock_map:
            stock_map[code] = {
                'stock_code': code,
                'buy_lot': 0,
                'sell_lot': 0,
                'buy_value': 0,
                'sell_value': 0,
                'buy_avg_price': 0,
                'sell_avg_price': 0,
                'investor_type': stock.get('investor_type', 'Unknown')
            }
        
        if stock['transaction_type'] == 'BUY':
            stock_map[code]['buy_lot'] += stock['lot']
            stock_map[code]['buy_value'] += stock['value_raw']
            stock_map[code]['buy_avg_price'] = stock['avg_price']
        else:  # SELL
            stock_map[code]['sell_lot'] += abs(stock['lot'])
            stock_map[code]['sell_value'] += abs(stock['value_raw'])
            stock_map[code]['sell_avg_price'] = stock['avg_price']
    
    # Calculate net positions
    result = []
    for code, data in stock_map.items():
        net_lot = data['buy_lot'] - data['sell_lot']
        net_value = data['buy_value'] - data['sell_value']
        
        # Calculate percentage change
        diff_pct = 0
        if data['buy_avg_price'] > 0 and data['sell_avg_price'] > 0:
            diff_pct = ((data['sell_avg_price'] - data['buy_avg_price']) / data['buy_avg_price']) * 100
        
        result.append({
            'stock_code': code,
            'buy_lot': int(data['buy_lot']),
            'sell_lot': int(data['sell_lot']),
            'net_lot': int(net_lot),
            'buy_value': data['buy_value'],
            'sell_value': data['sell_value'],
            'value_raw': net_value,
            'value': format_currency(abs(net_value)),
            'buy_avg_price': round(data['buy_avg_price'], 2),
            'sell_avg_price': round(data['sell_avg_price'], 2),
            'current_price': None,  # Will be populated by price API integration
            'diff_pct': round(diff_pct, 2),
            'investor_type': data['investor_type'],
            'position': 'NET BUY' if net_value > 0 else 'NET SELL' if net_value < 0 else 'NEUTRAL'
        })
    
    return result


def parse_number(value: Any) -> float:
    """Parse number from string or scientific notation."""
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        try:
            # Handle scientific notation
            return float(value)
        except ValueError:
            return 0.0
    
    return 0.0


def format_currency(amount: float) -> str:
    """Format currency in Indonesian Rupiah."""
    if amount >= 1_000_000_000_000:  # Trillion
        return f"Rp {amount / 1_000_000_000_000:.2f}T"
    elif amount >= 1_000_000_000:  # Billion
        return f"Rp {amount / 1_000_000_000:.2f}B"
    elif amount >= 1_000_000:  # Million
        return f"Rp {amount / 1_000_000:.2f}M"
    else:
        return f"Rp {amount:,.0f}"


def get_broker_name(broker_code: str) -> str:
    """Get broker full name from code."""
    broker_names = {
        'BK': 'Bank of America Merrill Lynch',
        'YP': 'Yuanta Securities',
        'ZP': 'Phillip Securities',
        'CS': 'Credit Suisse',
        'MS': 'Morgan Stanley',
        'GS': 'Goldman Sachs',
        # Add more broker mappings as needed
    }
    return broker_names.get(broker_code, f'Broker {broker_code}')


def validate_json_structure(data: Any) -> bool:
    """
    Validate that the JSON has the expected structure.
    """
    if isinstance(data, list):
        if not data:
            return False
        # Check first item
        item = data[0]
    elif isinstance(data, dict):
        item = data
    else:
        return False
    
    # Check required fields
    required_fields = ['broker', 'response']
    for field in required_fields:
        if field not in item:
            return False
    
    # Check response structure
    response = item.get('response', {})
    if 'data' not in response:
        return False
    
    data_obj = response.get('data', {})
    if 'broker_summary' not in data_obj:
        return False
    
    return True
