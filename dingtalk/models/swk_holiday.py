import requests, os ,json
from datetime import datetime
from bs4 import BeautifulSoup

CACHE_FILE = "sarawak_holidays.json"

class SwkHolidayAPI:

    def fetch_sarawak_holidays_en(year):
   
        url = f"https://publicholidays.com.my/sarawak/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print("Failed to download holiday page:", resp.status_code)
            return {}

        soup = BeautifulSoup(resp.text, "html.parser")
        holidays = {}


        year_header = soup.find(lambda tag: tag.name in ["h2", "h3"] and str(year) in tag.text)
        if not year_header:
            print(f"{year} table not found")
            return {}


        table = year_header.find_next("table")
        if not table:
            print(f"{year} table not found after header")
            return {}


        for tr in table.find_all("tr")[1:]:  # skip header row
            cols = tr.find_all("td")
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)
                days = cols[2].get_text(strip=True) if len(cols) > 2 else "Undefined"  
                try:
                    date_obj = datetime.strptime(f"{date_str} {year}", "%d %b %Y")
                    key = date_obj.strftime("%Y-%m-%d")
                    holidays[key] = {"name": name, "days": days}
                except Exception as e:
                    print("Date parsing error:", date_str, e)

        return holidays
    
    def load_holidays_en(year):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
            if str(year) in data:
                return data[str(year)]

        holidays = SwkHolidayAPI.fetch_sarawak_holidays_en(year)
        if holidays:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = {}
            data[str(year)] = holidays
            with open(CACHE_FILE, "w") as f:
                json.dump(data, f, indent=2)
        return holidays
    
    def is_holiday(date_str, holidays):
        if date_str in holidays:
            return True, holidays[date_str]
        return False, None