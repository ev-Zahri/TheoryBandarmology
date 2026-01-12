"""
Storage module for accumulation data
Handles JSON file operations
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


# Path to accumulation data file
DATA_DIR = Path(__file__).parent.parent.parent / "data"
ACCUMULATION_FILE = DATA_DIR / "stock_accumulation_data.json"


def save_accumulation_data(data: Dict[str, Any]) -> None:
    """
    Save accumulation data to JSON file
    
    Args:
        data: Accumulation data dictionary
    """
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON
    with open(ACCUMULATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Accumulation data saved: {len(data.get('brokers', {}))} brokers")


def load_accumulation_data() -> Dict[str, Any]:
    """
    Load accumulation data from JSON file
    
    Returns:
        Accumulation data dictionary, or empty dict if file doesn't exist
    """
    if not ACCUMULATION_FILE.exists():
        return {
            'last_updated': None,
            'total_brokers': 0,
            'brokers': {}
        }
    
    try:
        with open(ACCUMULATION_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Accumulation data loaded: {len(data.get('brokers', {}))} brokers")
        return data
    except Exception as e:
        print(f"Error loading accumulation data: {e}")
        return {
            'last_updated': None,
            'total_brokers': 0,
            'brokers': {}
        }


def clear_accumulation_data() -> None:
    """
    Clear/reset accumulation data
    """
    if ACCUMULATION_FILE.exists():
        ACCUMULATION_FILE.unlink()
    print("Accumulation data cleared")
