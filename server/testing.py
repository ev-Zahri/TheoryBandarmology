import requests
import pandas as pd
from datetime import datetime, timedelta

# Forex Factory menyediakan JSON publik per hari — tidak perlu API key
FF_BASE_URL = "https://nfs.faireconomy.media/ff_calendar_{year}{month:02d}{day:02d}.json"

def fetch_economic_calendar(start_date: datetime, end_date: datetime, impact_filter: str = "High") -> pd.DataFrame:
    all_events = []
    current = start_date

    while current <= end_date:
        url = FF_BASE_URL.format(year=current.year, month=current.month, day=current.day)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data:
                all_events.extend(data)
        except requests.HTTPError:
            print(f"Tidak ada data untuk: {current.date()}")
        except Exception as e:
            print(f"Error pada {current.date()}: {e}")
        current += timedelta(days=1)

    if not all_events:
        return pd.DataFrame()

    df = pd.DataFrame(all_events)

    # Filter berdasarkan impact jika diinginkan
    if impact_filter and "impact" in df.columns:
        df = df[df["impact"].str.contains(impact_filter, case=False, na=False)]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    start = datetime(2024, 1, 1)
    end   = datetime(2024, 1, 10)

    print(f"Mengambil kalender ekonomi dari {start.date()} hingga {end.date()}...\n")
    df = fetch_economic_calendar(start, end, impact_filter="High")

    if df.empty:
        print("Tidak ada event High impact ditemukan.")
    else:
        cols = [c for c in ["date", "time", "currency", "impact", "title", "forecast", "previous"] if c in df.columns]
        print(f"=== Economic Calendar (High Impact) — {len(df)} event ===\n")
        print(df[cols].to_string(index=False))

        df.to_csv("economic_calendar.csv", index=False)
        print("\nData tersimpan ke: economic_calendar.csv")
