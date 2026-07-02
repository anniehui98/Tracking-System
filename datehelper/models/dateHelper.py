from datetime import datetime,date ,timedelta

class FormatAPI:
    def __init__(self, value: int | float | str | date):
        self.value = self._to_datetime(value)

    @staticmethod
    def _to_datetime(value: int | float | str | date) -> datetime:
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date string: {value}. Use 'YYYY-MM-DD'.")
            
        if isinstance(value, (int, float)):
            if value > 1e12:
                value = value / 1000
            return datetime.fromtimestamp(value)
        raise TypeError(f"Unsupported type: {type(value)}")
    
    def date_time_format(self) -> str:
        return self.value.strftime("%Y-%m-%d %H:%M:%S")

    def date_only_format(self) -> str:
        return self.value.strftime("%Y-%m-%d")
    
    def date_day_format(self) -> str:
        return self.value.strftime("%Y-%m-%d（%A）")
    
    def time_only_format(self) -> str:
        return self.value.strftime("%H:%M:%S")
    


def split_date_range(start_date, end_date, max_days=7):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    ranges = []
    current = start
    while current <= end:
        temp_end = current + timedelta(days=max_days-1)
        if temp_end > end:
            temp_end = end
        ranges.append((current.strftime("%Y-%m-%d"), temp_end.strftime("%Y-%m-%d")))
        current = temp_end + timedelta(days=1)
    return ranges
    