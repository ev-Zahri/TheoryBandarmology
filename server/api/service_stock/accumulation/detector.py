"""
Stock Accumulation Detector
Detects stocks that appear in ALL transactions within the same broker
"""

from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict

# Import master data for sector/industry info
try:
    from api.service_stock.master_data import get_sector, get_stock_fundamental_data
except ImportError:
    # Fallback if master_data not available
    def get_sector(stock_code):
        return None
    def get_stock_fundamental_data(stock_code):
        return None


def detect_accumulation(broker_data_list: List[Dict]) -> Dict[str, Any]:
    """
    Detect stocks that appear in 100% of transactions for each broker
    
    Args:
        broker_data_list: List of broker data entries from uploaded JSON
        
    Returns:
        Dictionary with accumulation results per broker
    """
    # Group data by broker
    broker_transactions = defaultdict(list)
    
    for entry in broker_data_list:
        broker_code = entry.get('broker', 'UNKNOWN')
        broker_summary = entry.get('response', {}).get('data', {}).get('broker_summary', {})
        
        if not broker_summary:
            continue
            
        # Extract stocks from buy and sell (net position)
        stocks_in_transaction = set()
        
        # From brokers_buy
        for buy_entry in broker_summary.get('brokers_buy', []):
            stock_code = buy_entry.get('netbs_stock_code')
            if stock_code:
                stocks_in_transaction.add(stock_code)
        
        # From brokers_sell
        for sell_entry in broker_summary.get('brokers_sell', []):
            stock_code = sell_entry.get('netbs_stock_code')
            if stock_code:
                stocks_in_transaction.add(stock_code)
        
        # Store transaction data
        if stocks_in_transaction:
            transaction_date = entry.get('periode', {}).get('from', 'unknown')
            broker_transactions[broker_code].append({
                'date': transaction_date,
                'stocks': stocks_in_transaction,
                'buy_data': broker_summary.get('brokers_buy', []),
                'sell_data': broker_summary.get('brokers_sell', [])
            })
    
    # Analyze each broker
    results = {
        'last_updated': datetime.now().isoformat(),
        'total_brokers': len(broker_transactions),
        'brokers': {}
    }
    
    for broker_code, transactions in broker_transactions.items():
        total_transactions = len(transactions)
        
        # Count stock appearances
        stock_appearances = defaultdict(lambda: {
            'count': 0,
            'dates': [],
            'buy_volumes': [],
            'sell_volumes': [],
            'buy_values': [],
            'sell_values': []
        })
        
        for transaction in transactions:
            for stock_code in transaction['stocks']:
                stock_appearances[stock_code]['count'] += 1
                stock_appearances[stock_code]['dates'].append(transaction['date'])
                
                # Get volume and value data
                for buy_entry in transaction['buy_data']:
                    if buy_entry.get('netbs_stock_code') == stock_code:
                        try:
                            volume = float(buy_entry.get('blot', 0))
                            value = float(buy_entry.get('bval', 0))
                            stock_appearances[stock_code]['buy_volumes'].append(volume)
                            stock_appearances[stock_code]['buy_values'].append(value)
                        except (ValueError, TypeError):
                            pass
                
                for sell_entry in transaction['sell_data']:
                    if sell_entry.get('netbs_stock_code') == stock_code:
                        try:
                            volume = float(sell_entry.get('slot', 0))
                            value = float(sell_entry.get('sval', 0))
                            stock_appearances[stock_code]['sell_volumes'].append(volume)
                            stock_appearances[stock_code]['sell_values'].append(value)
                        except (ValueError, TypeError):
                            pass
        
        # Filter stocks with 100% appearance rate
        accumulating_stocks = []
        
        for stock_code, data in stock_appearances.items():
            appearance_rate = (data['count'] / total_transactions) * 100
            
            if appearance_rate == 100.0:
                # Calculate totals
                total_buy_volume = sum(data['buy_volumes'])
                total_sell_volume = sum(data['sell_volumes'])
                total_buy_value = sum(data['buy_values'])
                total_sell_value = sum(data['sell_values'])
                
                net_volume = total_buy_volume - total_sell_volume
                net_value = total_buy_value - total_sell_value
                
                # Calculate average price
                total_volume = total_buy_volume + total_sell_volume
                total_value = total_buy_value + total_sell_value
                avg_price = (total_value / total_volume) if total_volume > 0 else 0
                
                # Get sector and industry from master data
                sector = get_sector(stock_code)
                fundamental_data = get_stock_fundamental_data(stock_code)
                industry = None
                if fundamental_data:
                    industry = fundamental_data.get('industry')
                
                accumulating_stocks.append({
                    'stock_code': stock_code,
                    'sector': sector or 'Unknown',
                    'industry': industry or 'Unknown',
                    'appearances': data['count'],
                    'appearance_rate': appearance_rate,
                    'total_transactions': total_transactions,
                    'buy_volume': int(total_buy_volume),
                    'sell_volume': int(total_sell_volume),
                    'net_volume': int(net_volume),
                    'buy_value': int(total_buy_value),
                    'sell_value': int(total_sell_value),
                    'net_value': int(net_value),
                    'avg_price': round(avg_price, 2),
                    'first_seen': min(data['dates']),
                    'last_seen': max(data['dates']),
                    'transaction_dates': sorted(list(set(data['dates'])))
                })
        
        # Sort by net volume (descending)
        accumulating_stocks.sort(key=lambda x: abs(x['net_volume']), reverse=True)
        
        results['brokers'][broker_code] = {
            'broker_code': broker_code,
            'total_transactions': total_transactions,
            'total_stocks_analyzed': len(stock_appearances),
            'accumulating_stocks_count': len(accumulating_stocks),
            'accumulating_stocks': accumulating_stocks
        }
    
    return results


def get_all_accumulating_stocks(accumulation_data: Dict) -> List[Dict]:
    """
    Get flattened list of all accumulating stocks across all brokers
    """
    all_stocks = []
    
    for broker_code, broker_data in accumulation_data.get('brokers', {}).items():
        for stock in broker_data.get('accumulating_stocks', []):
            all_stocks.append({
                **stock,
                'broker_code': broker_code
            })
    
    # Sort by absolute net volume
    all_stocks.sort(key=lambda x: abs(x['net_volume']), reverse=True)
    
    return all_stocks


def get_broker_accumulation(accumulation_data: Dict, broker_code: str) -> Dict:
    """
    Get accumulation data for specific broker
    """
    return accumulation_data.get('brokers', {}).get(broker_code, {})
