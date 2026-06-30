from datetime import datetime

def parse_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        value = value.strip()
        for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%d.%m.%y', '%Y/%m/%d'):
            try:
                dt = datetime.strptime(value, fmt)
                return dt.date()
            except ValueError:
                continue
    return None
