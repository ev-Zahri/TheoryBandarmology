import csv
import json

def convert_stock_csv_to_json(csv_path, json_path):
    """
    Convert stock_wiki.csv to a compact JSON format for news crawling
    
    Output format:
    {
        "stocks": [
            {
                "code": "AALI",
                "name": "Astra Agro Lestari",
                "sector": "Consumer Non-Cyclicals"
            },
            ...
        ],
        "by_sector": {
            "Consumer Non-Cyclicals": ["AALI", "ADES", ...],
            ...
        }
    }
    """
    stocks = []
    by_sector = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Extract ticker code (remove "BEI: " prefix)
                kode_raw = row['Kode'].strip()
                ticker = kode_raw.replace('BEI: ', '').replace('BEI:', '').strip()
                
                # Clean company name (remove "Tbk." suffix for cleaner matching)
                nama = row['Nama perusahaan'].strip()
                nama_clean = nama.replace(' Tbk.', '').replace(' Tbk', '').strip()
                
                # Get sector
                sektor = row['Sektor'].strip()
                
                # Add to stocks list
                stock_entry = {
                    "code": ticker,
                    "name": nama_clean,
                    "sector": sektor
                }
                stocks.append(stock_entry)
                
                # Group by sector
                if sektor not in by_sector:
                    by_sector[sektor] = []
                by_sector[sektor].append(ticker)
        
        # Create final structure
        output = {
            "total_stocks": len(stocks),
            "stocks": stocks,
            "by_sector": by_sector,
            "sectors": list(by_sector.keys())
        }
        
        # Write to JSON
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(output, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted {len(stocks)} stocks to JSON")
        print(f"📊 Total sectors: {len(by_sector)}")
        print(f"💾 Output saved to: {json_path}")
        
        # Print sector summary
        print("\n📈 Stocks per sector:")
        for sector, tickers in sorted(by_sector.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  - {sector}: {len(tickers)} stocks")
        
        return output
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    csv_file = "stock_wiki.csv"
    json_file = "stocks_data.json"
    
    result = convert_stock_csv_to_json(csv_file, json_file)
    
    if result:
        print(f"\n✨ Sample data:")
        print(json.dumps(result['stocks'][:5], indent=2, ensure_ascii=False))
