from datetime import datetime, timedelta

def build_calendar(dates, times, employee_name):
    if not dates:
        raise ValueError("Список дат пуст")

    # Словарь: дата -> время
    pairs = {date: time for date, time in zip(dates, times)}
    
    # Определим месяц и год из первой даты (предполагаем, что все даты одного месяца)
    first_date = min(dates)
    year = first_date.year
    month = first_date.month

    # Первый и последний день месяца
    start_of_month = datetime(year, month, 1).date()
    if month == 12:
        next_month = datetime(year+1, 1, 1).date()
    else:
        next_month = datetime(year, month+1, 1).date()
    end_of_month = next_month - timedelta(days=1)

    # Начало недели, содержащей 1-е число (понедельник)
    start_of_week = start_of_month - timedelta(days=start_of_month.weekday())
    # Конец недели, содержащей последний день месяца (воскресенье)
    end_of_week = end_of_month + timedelta(days=(6 - end_of_month.weekday()))

    weeks = []
    current_week = []
    current = start_of_week

    while current <= end_of_week:
        # Если дата принадлежит текущему месяцу – берём время из словаря (или None, если нет)
        if start_of_month <= current <= end_of_month:
            time = pairs.get(current, (None, None))
            is_in_range = True
        else:
            # Дни из соседних месяцев – показываем как прочерки
            time = (None, None)
            is_in_range = False

        current_week.append({
            'date': current,
            'time': time,
            'is_in_range': is_in_range
        })

        if current.weekday() == 6:  # воскресенье
            weeks.append(current_week)
            current_week = []
        current += timedelta(days=1)

    if current_week:
        weeks.append(current_week)

    period_start = start_of_month.strftime('%d.%m.%Y')
    period_end = end_of_month.strftime('%d.%m.%Y')

    return {
        'employee_name': employee_name,
        'period_start': period_start,
        'period_end': period_end,
        'weeks': weeks
    }