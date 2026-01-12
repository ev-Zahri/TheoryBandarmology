"""
Master Data Module
Provides access to technical and fundamental stock data
"""

from .technical_loader import (
    load_technical_data,
    save_technical_data,
    get_stock_technical_data,
    get_current_price,
    get_multiple_prices,
    is_data_stale as is_technical_stale,
    get_data_age as get_technical_age,
    get_stats as get_technical_stats
)

from .fundamental_loader import (
    load_fundamental_data,
    save_fundamental_data,
    get_stock_fundamental_data,
    get_sector,
    get_financial_ratios,
    get_company_profile,
    is_data_stale as is_fundamental_stale,
    get_data_age as get_fundamental_age,
    get_stats as get_fundamental_stats,
    get_all_sectors
)

from .data_updater import (
    get_all_stock_codes,
    update_technical_data_batch,
    update_fundamental_data_batch,
    add_stocks_from_broker_data
)

__all__ = [
    # Technical data
    'load_technical_data',
    'save_technical_data',
    'get_stock_technical_data',
    'get_current_price',
    'get_multiple_prices',
    'is_technical_stale',
    'get_technical_age',
    'get_technical_stats',
    
    # Fundamental data
    'load_fundamental_data',
    'save_fundamental_data',
    'get_stock_fundamental_data',
    'get_sector',
    'get_financial_ratios',
    'get_company_profile',
    'is_fundamental_stale',
    'get_fundamental_age',
    'get_fundamental_stats',
    'get_all_sectors',
    
    # Data updater
    'get_all_stock_codes',
    'update_technical_data_batch',
    'update_fundamental_data_batch',
    'add_stocks_from_broker_data'
]
