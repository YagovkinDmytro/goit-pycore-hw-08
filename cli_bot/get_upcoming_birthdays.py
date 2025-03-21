from datetime import datetime, timedelta


def get_upcoming_birthdays(records):
    upcoming_birthdays = []
    today = datetime.now().date()
    date_interval = today + timedelta(days=7)
    
    for record in records:
        if record.birthday:
            birth_date = record.birthday.value
            print(str(birth_date))
            congratulation_date = datetime(today.year, birth_date.month, birth_date.day,).date()
            day_of_week = congratulation_date.weekday()

        if congratulation_date < today:
            congratulation_date = datetime(today.year + 1, birth_date.month, birth_date.day).date()

        if today <= congratulation_date <= date_interval:
            if day_of_week == 5:
                congratulation_date += timedelta(days=2)
            elif day_of_week == 6:
                congratulation_date += timedelta(days=1)
            
            congratulation_date_str = congratulation_date.strftime("%d.%m.%Y")
            upcoming_birthdays.append({"name": record.name.value, "birthday": congratulation_date_str})
    
    return upcoming_birthdays