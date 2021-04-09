
import datetime
from datetime import timedelta, date, time

import numpy
import numpy as np
# returns lists of water usage calculations for each day jan 1 - april 30

dates = []
string_dates = []

shower_gal = []
bath_gal = []
shower_hot_gal = []
bath_hot_gal = []

dishes_gal = []
dishes_hot_gal = []
laundry_gal = []
laundry_hot_gal = []

shower_strings = []
bath_strings = []

dishes_strings = []
laundry_strings = []


def daterange():

    start_dt = date(2021, 1, 1)  # jan 1st
    end_dt = date(2021, 4, 30)  # april 30th

    for n in range(int((end_dt - start_dt).days)+1):
        yield start_dt + timedelta(n)


def create_dates():

    for dt in daterange():
        date = dt  # date objects to use in calculating weekdays
        string_date = dt.strftime("%Y-%m-%d")  # string of dates to use in final list
        dates.append(date)
        string_dates.append(string_date)
    return dates, string_dates


def shower_and_bath():

    daterange()
    create_dates()

    gal_per_shower = 25
    hot_per_shower = 16.25

    gal_per_bath = 30
    hot_per_bath = 19.5

    for i in dates:
        # print(i.weekday())
        if i.weekday() <= 4:  # weekdays
            total_shower_gallons = (gal_per_shower*3)
            total_shower_hot = (hot_per_shower*3)

            total_bath_gallons = (gal_per_bath*3)
            total_bath_hot = (hot_per_bath * 3)

            shower_gal.append(total_shower_gallons)
            shower_hot_gal.append(total_shower_hot)
            bath_gal.append(total_bath_gallons)
            bath_hot_gal.append(total_bath_hot)

            shower_strings.append('shower')
            bath_strings.append('bath')

        if i.weekday() > 4:  # weekends
            total_shower_gallons = (gal_per_shower*2)
            total_shower_hot = (hot_per_shower*2)

            total_bath_gallons = (gal_per_bath*2)
            total_bath_hot = (hot_per_bath * 2)

            shower_gal.append(total_shower_gallons)
            shower_hot_gal.append(total_shower_hot)
            bath_gal.append(total_bath_gallons)
            bath_hot_gal.append(total_bath_hot)

            shower_strings.append('shower')
            bath_strings.append('bath')

    return (shower_gal, shower_hot_gal, bath_gal, bath_hot_gal, shower_strings, bath_strings)


def dishes_and_laundry():
    # happen 4 times a week - Monday(0), Wednesday(2), Friday(4), and Sunday(6)
    daterange()
    create_dates()

    gal_per_dishes = 6
    hot_per_dishes = 6

    gal_per_laundry = 20
    hot_per_laundry = 17

    for i in dates:
        # print(i.weekday())
        if i.weekday() == 0 or i.weekday() == 2 or i.weekday() == 4 or i.weekday() == 6:  # weekdays
            total_dishes_gallons = (gal_per_dishes)
            total_dishes_hot = (hot_per_dishes)

            total_laundry_gallons = (gal_per_laundry)
            total_laundry_hot = (hot_per_laundry)

            dishes_gal.append(total_dishes_gallons)
            dishes_hot_gal.append(total_dishes_hot)
            laundry_gal.append(total_laundry_gallons)
            laundry_hot_gal.append(total_laundry_hot)

            dishes_strings.append('dishes')
            laundry_strings.append('laundry')

        else:
            total_dishes_gallons = 0
            total_dishes_hot = 0

            total_laundry_gallons = 0
            total_laundry_hot = 0

            dishes_gal.append(total_dishes_gallons)
            dishes_hot_gal.append(total_dishes_hot)
            laundry_gal.append(total_laundry_gallons)
            laundry_hot_gal.append(total_laundry_hot)

            dishes_strings.append('dishes')
            laundry_strings.append('laundry')

    return (dishes_gal, dishes_hot_gal, laundry_gal, laundry_hot_gal, dishes_strings, laundry_strings)

def calculate_water_usage():
    daterange()
    shower_and_bath()
    dishes_and_laundry()

    total_gallons = [a + b + c + d for a, b, c, d in zip(shower_gal, bath_gal, dishes_gal, laundry_gal)]
    total_gallons_daily = [list(e) for e in zip(string_dates, total_gallons)]

    total_hot = [w + x + y + z for w, x, y, z in zip(shower_hot_gal, bath_hot_gal, dishes_hot_gal, laundry_hot_gal)]  # gives total gallons of hot water used
    total_hot_daily = [list(e) for e in zip(string_dates, total_hot)]

    total_water_records =  [tuple(e) for e in zip (string_dates, total_gallons, total_hot)]
    print("\n.....................................................................................")
    print(f"Timestamp of this run: {datetime.datetime.now()}")
    print("\n.....................................................................................")
    print("\nExecuted water_calculations.main function, which handles the following calculations:")
    print("\ntotal_gallons_daily\n total gallons\n total_hot\n and total_hot_daily")
    print(f"\n      _______________ \n        total_gallons\n      _______________\n{total_gallons}\n")
    print(f"\n      _______________ \n        total_gallons_daily\n      _______________\n{total_gallons_daily}")
    print(f"\n      _______________ \n       total_hot\n      _______________\n{total_hot}\n")
    print(f"\n      _______________ \n       total_hot_daily\n      _______________\n {total_hot_daily}")



    print("~~~~~~~~~`\n\ndate, total_gallons, hot_gallons\n\n" ,total_water_records,"\n\n~~~~~~~~~~~~~`")



    print("\n.....................................................................................")

    return total_water_records

