import pandas as pd
from datetime import datetime
from utils.date_helpers import parse_date
from utils.time_helpers import parse_time_interval

def parse_excel(file_stream):
    df = pd.read_excel(file_stream, header=None)
    print("Размер df:", df.shape)
    if df.empty:
        raise ValueError("Файл пуст")
    
    header_row = df.iloc[0].values
    print("Заголовок (первые 10):", header_row[:10])
    if df.shape[0] < 2:
        raise ValueError("Неверный формат: отсутствует строка с данными")
    data_row = df.iloc[1].values

    employee_name = str(data_row[0]).strip() if data_row[0] is not None else ""
    if not employee_name:
        raise ValueError("Не удалось найти ФИО сотрудника")

    dates = []
    times = []

    for i in range(1, len(header_row)):
        date_val = header_row[i]
        time_val = data_row[i] if i < len(data_row) else None

        print(f"Обработка столбца {i}: date_val={date_val} (тип {type(date_val)})")

        if isinstance(date_val, datetime):
            dt = date_val.date()
            print(f"  -> это datetime, dt={dt}")
        else:
            dt = parse_date(date_val)
            print(f"  -> parse_date вернул {dt}")

        if dt is not None:
            dates.append(dt)
            start, end = parse_time_interval(time_val)
            times.append((start, end))
        else:
            # Если дата не распознана – возможно, это пустая ячейка или недата
            # Но мы не хотим пропускать даты, поэтому для отладки выведем предупреждение
            print(f"  !!! Дата не распознана: {date_val}")

    print("Все даты:", [d.strftime('%d.%m') for d in dates])
    if not dates:
        raise ValueError("Не найдено ни одной даты в заголовке")

    while len(times) < len(dates):
        times.append((None, None))

    return {
        'employee_name': employee_name,
        'dates': dates,
        'times': times
    }