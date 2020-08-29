import django
import os
import logging
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sangster_math.settings.__init__")
django.setup()

from .models import Day

import datetime
import sys

start_year = int(sys.argv[1])
weekday_of_sep_1 = int(sys.argv[2])

DAYS = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}

# python -m sangster_math.apps.schedule.create {start_year(int)} {weekday_of_sep_1(int)}
# create a day for each date between September 1, {start_year} and August 31, {start_year + 1}

# September
for d in range(30):
    date = datetime.date(start_year, 9, d + 1)
    new_day = Day(date=date, month="September", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# October
for d in range(31):
    date = datetime.date(start_year, 10, d + 1)
    new_day = Day(date=date, month="October", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# November
for d in range(30):
    date = datetime.date(start_year, 11, d + 1)
    new_day = Day(date=date, month="November", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# December
for d in range(31):
    date = datetime.date(start_year, 12, d + 1)
    new_day = Day(date=date, month="December", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# January
for d in range(31):
    date = datetime.date(start_year + 1, 1, d + 1)
    new_day = Day(date=date, month="January", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# February
num_days = 28
if start_year + 1 % 4 == 0:
    num_days = 29
for d in range(num_days):
    date = datetime.date(start_year + 1, 2, d + 1)
    new_day = Day(date=date, month="February", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# March
for d in range(31):
    date = datetime.date(start_year + 1, 3, d + 1)
    new_day = Day(date=date, month="March", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# April
for d in range(30):
    date = datetime.date(start_year + 1, 4, d + 1)
    new_day = Day(date=date, month="April", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# May
for d in range(31):
    date = datetime.date(start_year + 1, 5, d + 1)
    new_day = Day(date=date, month="May", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# June
for d in range(30):
    date = datetime.date(start_year + 1, 6, d + 1)
    new_day = Day(date=date, month="June", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# July
for d in range(31):
    date = datetime.date(start_year + 1, 7, d + 1)
    new_day = Day(date=date, month="July", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()

# August
for d in range(31):
    date = datetime.date(start_year + 1, 8, d + 1)
    new_day = Day(date=date, month="August", weekday=DAYS[weekday_of_sep_1 % 7])
    weekday_of_sep_1 += 1
    new_day.save()
