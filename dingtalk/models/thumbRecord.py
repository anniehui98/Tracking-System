import requests
from .tokenManager import get_token
from datehelper import split_date_range

class RecordAPI:

    def __init__(self, u_id: str,start_date: str,end_date: str):
        self.user_id = u_id
        self.start = start_date
        self.end = end_date
        self.base_url = "https://oapi.dingtalk.com"
        self.headers = {"Content-Type": "application/json"}
            
    def get_thumb_record(self) -> dict:
            access_token = get_token()
            all_records = []

            date_ranges = split_date_range(self.start, self.end)

            for s_date, e_date in date_ranges:
                offset = 0
                limit = 50

                while True:
                    payload = {
                        "workDateFrom": f"{s_date} 00:00:00",
                        "workDateTo": f"{e_date} 23:59:59",
                        "offset": offset,
                        "limit": limit,
                        "userIdList": [self.user_id],
                        "isI18n": False
                    }

                    url= f"{self.base_url}/attendance/list?access_token={access_token}"
                    response = requests.post(url, json=payload, headers=self.headers)

                    try:
                        result = response.json()
                    except Exception as e:
                        print(f"Error parsing JSON: {e}, Response text: {response.text}")
                        break
            
                    records = result.get("recordresult", [])
                    if not records:
                        break

                    all_records.extend(records)

                    if len(records) < limit:
                        break

                    offset += limit

            return {"recordresult": all_records}
        