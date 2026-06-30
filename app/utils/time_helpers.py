import re

def parse_time_interval(value):
    """
    Разбирает строку вида "ЧЧ:ММ:СС - ЧЧ:ММ:СС" или с "****".
    Возвращает кортеж (start, end), где каждый элемент – строка "ЧЧ:ММ" или "****" или None.
    """
    if not value or not isinstance(value, str):
        return (None, None)

    value = value.strip()
    pattern = r'^\s*(.+?)\s*-\s*(.+?)\s*$'
    match = re.match(pattern, value)
    if not match:
        return (None, None)

    start_str = match.group(1).strip()
    end_str = match.group(2).strip()

    def to_hhmm(s):
        if s == '****':
            return '****'
        parts = s.split(':')
        if len(parts) >= 2:
            return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
        return None

    return (to_hhmm(start_str), to_hhmm(end_str))