import json
import urllib
import urllib.request
import psycopg2
import water_calculations
from datetime import datetime, date, time, timedelta
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from settings import settings
from water_calculations import *
####################################################
#   Environment Variables
####################################################
API_KEY = settings["METEOSTAT_API_KEY"]
WEATHER_STATION_ID = settings["WEATHER_STATION"]
database_params = settings["DB_PARAMS"]
CONNECTION = psycopg2.connect(**database_params)
########################################
'''API Info & Metadata, setup, etc.'''
########################################
app = FastAPI(title="ButlerAPI",  # App declared, also sets up API docs.
              description="Weather Functionality Near-Complete. Water Calculations incorporated. TODO--> Fix electricity endpoints. April 2021. API by Will Watts",
              version="0.5.1")
tags_metadata = settings["TAGS_METADATA"]
app = FastAPI(openapi_tags=tags_metadata)
#########################################
'''
........................................................................................................................
        Note on Endpoints and JSON:
 General Pattern of how most of these endpoints set up JSON: --> # for each loop i in raw_ result, form key/value pairs.
 key = daily_key, which is the date
 value = daily_value, which is a dict of weather stats for each date in table.
 daily_values is the resulting key value pair... example: { daily_key: {tavg, tmin, tmax, prcp} }
.........................................................................................................................
                                    Start of Endpoint Section
'''
#   ENDPOINT
#   HTTP GET for API root endpoint located at ".../"
#   Redirects to "/docs" endpoint, which is the Swagger documentation since that's probably where you're trying to go.
@app.get("/", tags=["openapi"])
async def root():
    # redirect to SwaggerAPI docs page so whoever is using this can test endpoints
    response = RedirectResponse(url='http://localhost:8000/docs')
    print("Redirected GET request at root endpoint to Swagger API Documentation endpoint")
    return response

@app.get("/openapi.json", tags=["openapi"])
async def get_open_api_json_spec():
    # redirect to SwaggerAPI docs page so whoever is using this can test endpoints
    response = RedirectResponse(url='http://localhost:8000/openapi.json')
    return response

@app.get("/weather/daily/all", tags=["weather", "daily"])
async def get_all_weather_values():
    db_cursor = CONNECTION.cursor()                             # psycopg2 cursor object
    db_cursor.execute('select * FROM "daily_weather_data";')           # execute SQL command
    raw_result = db_cursor.fetchall()                           # fetch command result
    db_cursor.close()                                           # close to prevent leaks
    response_value = []                 # outer object, dicts within

    for i in raw_result:
        daily_values = {}               # key/value pairs within JSON response
        daily_key = str(i[0])           # date ... key for a key/value pair within JSON
        daily_value = {}                # value values for key for a key/value pair
        daily_value["tavg"] = i[1]      # average temperature in celsius
        daily_value["tmin"] = i[2]      # min temperature in celsius
        daily_value["tmax"] = i[3]      # max temperature in celsius
        daily_value["prcp"] = i[4]      # precipitation in mm
        daily_values[daily_key] = daily_value           # now bind these key/value pairs --> formats each date's record data
        response_value.append(daily_values)             # the resulting daily_values for each iteration is appended to response_value
    json_response = {"records": response_value}     # JSON response, final result
    return json_response


# ENDPOINT Api Endpoint: Retrieves **all** records in daily_weather_data Table
@app.get('/weather/daily/{selectedDate}', tags=["weather", "daily"])
async def get_a_weather_values_by_date(selectedDate: str):
    selectedDate = datetime.fromisoformat(selectedDate).date()
    db_cursor = CONNECTION.cursor()
    db_cursor.execute(
        'SELECT * FROM "daily_weather_data" WHERE date = %s', (selectedDate,))
    raw_result = db_cursor.fetchall()
    db_cursor.close()
    response_value = []

    for i in raw_result:
        daily_values = {}               # key/value pairs within JSON response
        daily_key = str(i[0])           # date ... key for a key/value pair within JSON
        daily_value = {}                # value values for key for a key/value pair
        daily_value["tavg"] = i[1]      # average temperature
        daily_value["tmin"] = i[2]      # min temperature
        daily_value["tmax"] = i[3]      # max temperature
        daily_value["prcp"] = i[4]      # precipitation
        daily_values[daily_key] = daily_value
        response_value.append(daily_values)
    json_response = {"records": response_value}     # JSON response, final result
    return json_response

# ENDPOINT --> create new record ... each must have unique date, date is Pkey
@app.post('/weather/daily/{newRecordDate}/{avgT}/{minT}/{maxT}/{precip}', tags=["weather", "daily"])
async def create_weather_values(newRecordDate: str,
                                avgT: float,
                                minT: float,
                                maxT: float,
                                precip: float
                                ):

    newRecordDate = datetime.fromisoformat(newRecordDate).date()
    db_cursor = CONNECTION.cursor()
    db_cursor.execute(
        '''
        INSERT INTO "daily_weather_data" (date, tavg, tmin, tmax, prcp)
        VALUES (%s, %s, %s, %s, %s);
        ''', (newRecordDate, avgT, minT, maxT, precip))
    message = (
        f"successfully executed INSERT(date {newRecordDate}, tavg {avgT}, tmin {minT}, tmax {maxT}, prcp {precip})")
    CONNECTION.commit(),
    return {"msg": [message]}


# ENDPOINT --> Delete Weather record by date
@app.delete('/weather/daily/{dateToDelete}', tags=["weather", "daily"])
async def delete_weather_values(dateToDelete: str):
    db_cursor = CONNECTION.cursor()
    db_cursor.execute('DELETE FROM "daily_weather_data" WHERE date = %s RETURNING *;', (dateToDelete,))
    message = (
        f"successfully deleted record for {dateToDelete}")
    CONNECTION.commit(),
    return {"msg": [message]}


@app.get("/weather/daily/all", tags=["weather", "daily"])
async def get_all_weather_valuess():
    db_cursor = CONNECTION.cursor()                             # <- psycopg2 cursor object
    db_cursor.execute('select * FROM "daily_weather_data";')    # <- execute SQL command
    raw_result = db_cursor.fetchall()                           # <-fetch command result
    db_cursor.close()                                           # <- close to prevent leaks
    response_value = []                                         # <- outer object, dicts within

    for i in raw_result:
        # { daily_key: {tavg, tmin, tmax, prcp} } <--- one for each date in JSON
        daily_values = {}               # key/value pairs within JSON response
        daily_key = str(i[0])           # date ... key for a key/value pair within JSON
        daily_value = {}                # value values for key for a key/value pair
        daily_value["tavg"] = i[1]      # average temperature in celsius
        daily_value["tmin"] = i[2]      # min temperature celsius
        daily_value["tmax"] = i[3]      # max temperature celsius
        daily_value["prcp"] = i[4]      # precipitation in mm
        daily_values[daily_key] = daily_value
        response_value.append(daily_values)
    json_response = {"records": response_value}     # JSON response, final result
    return json_response


@app.get('/weather/hourly/all', tags=["weather", 'hourly'])
async def get_all_hourly_weather_records_stored_in_butler_api_database():
    db_cursor = CONNECTION.cursor()                             # psycopg2 cursor object
    db_cursor.execute('select * FROM "hourly_weather_data";')   # execute SQL command
    raw_result = db_cursor.fetchall()                           # fetch command result
    db_cursor.close()                                           # close to prevent leaks
    response_value = []                 # JSON's outer list, dicts within
    for i in raw_result:                # each hour has a dictionary of values of different weather stats. ({key: value})
        hourly_value = {}
        hourly_values = {}
        hourly_key = i[0]
        hourly_value["recDate"] = i[1]
        hourly_value["recHour"] = i[2]
        hourly_value["temp"] = i[3]
        hourly_value["dwpt"] = i[4]
        hourly_value["rhum"] = i[5]
        hourly_value["prcp"] = i[6]
        hourly_value["snow"] = i[7]
        hourly_value["wdir"] = i[8]
        hourly_value["wspd"] = i[9]
        hourly_value["wpgt"] = i[10]
        hourly_value["pres"] = i[11]
        hourly_value["tsun"] = i[12]
        hourly_value["coco"] = i[13]
        # now bind these key/value pairs --> formats each date's record data
        hourly_values[hourly_key] = hourly_value    # map the timestamp to the values dictionary from above.
        # the resulting daily_values for each iteration is appended to response_value
        response_value.append(hourly_values)        # the newly made dictionary is added to the list for our JSON response.
    json_response = {"records": response_value}     # JSON response, final result
    return json_response


# ENDPOINT
@app.post('/weather/meteostat_api_data/hourly/{startDate}/{endDate}', tags=["weather", "hourly"])
async def fetch_and_post_meteostat_api_hourly_weather_data_for_up_to_ten_day_date_range(startDate: str, endDate: str):
    api_key_header = {'x-api-key': API_KEY}                 # required by Meteostat API. This authorizes query to their JSON API.
    url = "https://api.meteostat.net/v2/stations/hourly?station="+WEATHER_STATION_ID+"&start="+startDate+"&end="+endDate
    # req is the request (arg1= the target url, arg2= x-api-key header required by Meteostat's JSON API as an Authorization header)
    req = urllib.request.Request(url, headers=api_key_header)   # See comment on line above.
    r = urllib.request.urlopen(req)
    hourly_data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))  # don't touch this. This converts fetched API for us.
    meteostat_api_json_response = hourly_data["data"]     # JSON response from Meteostat API (remote API)
    records = []                                            # will hold list of hourly_record dictionaries, with timestamps as keys.
    for entry in meteostat_api_json_response:
        hourly_record = {}                                  # will hold key/value pairs of { timestamp: hourly_values}
        hourly_values = {}                                  # will hold key/value pairs of {stat name: stat value}
        hourly_key = datetime.fromisoformat(entry["time"])  # the timestamp, which is date and time
        hourly_values["recDate"] = hourly_key.date()        # just the date of the timestamp
        hourly_values["recHour"] = hourly_key.time()        # just the hour/time of the timestamp
        hourly_values["temp"] = entry["temp"]               # temp in degrees celsius
        hourly_values["dwpt"] = entry["dwpt"]               # dew point in degrees celsius
        hourly_values["rhum"] = entry["rhum"]               # relative humidity
        hourly_values["prcp"] = entry["prcp"]               # precipitation in mm
        hourly_values["snow"] = entry["snow"]               # snow in mm
        hourly_values["wdir"] = entry["wdir"]               # wind direction in degrees (0-359 degrees, compass)
        hourly_values["wspd"] = entry["wspd"]               # wind speed in KM/H
        hourly_values["wpgt"] = entry["wpgt"]               # wind peak gust in KM/H
        hourly_values["pres"] = entry["pres"]               # pressure
        hourly_values["tsun"] = entry["tsun"]               # time of sunlight?
        hourly_values["coco"] = entry["coco"]               # weather condition code ... COCO = condition code.
        hourly_record = {hourly_key: hourly_values}         # form key value pair between timestamp and the hourly values for it
        records.append(hourly_record)                       # append key value pair from line above to records list.
        db_cursor = CONNECTION.cursor()                     # db_cursor is psycopg2 cursor.
        db_cursor.execute(                                  # Execute the SQL command in the 3x single-quote block below.
            '''
            INSERT INTO "hourly_weather_data" (timestamp, rec_date, rec_hour, temp, dwpt, rhum, prcp, snow, wdir, wspd, wpgt, pres, tsun, coco)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''',
            ((
                hourly_key, hourly_values["recDate"], hourly_values["recHour"], hourly_values["temp"], hourly_values["dwpt"], hourly_values["rhum"],
                hourly_values["prcp"], hourly_values["snow"], hourly_values["wdir"], hourly_values["wspd"], hourly_values["wpgt"], hourly_values["pres"], hourly_values["tsun"], hourly_values["coco"]
            )))
    # note on above: %s is converted to value in psycopg2. Yes, it should be %s regardless of type. Never use %d, etc for psycopg2 per official docs.
    # The values after the 3x single quote block are mapped tothe %s in the same order they appear.
    CONNECTION.commit()                             # add and save these changes to database.
    db_cursor.close()                               # close cursor to prevent leaks.
    result = {"hourly_records": records}            # This is json response.
    message = ("successfully executed INSERT INTO \"hourly_weather_data\" (timestamp, rec_date, rec_hour, temp, dwpt, rhum, "+"prcp, snow, wdir, wspd, wpgt, pres, tsun, coco", result)
    return message

# DELETE ("D" in "CRUD")
# ENDPOINT --> Delete All Hourly Weather Records for a specified date
@app.delete('/weather/hourly/{dateToDelete}', tags=["weather", "hourly"])
async def delete_hourly_weather_records_for_selected_date(dateToDelete: str):

    db_cursor = CONNECTION.cursor()
    db_cursor.execute('DELETE FROM "hourly_weather_data" WHERE rec_date = %s RETURNING *;', (dateToDelete,))
    message = (
        f"successfully deleted all records for {dateToDelete}")
    CONNECTION.commit(),
    return {"msg": [message]}



'''                        
                                START OF WATER SECTION
  CRUD = Creat (Http POST), Read(Http GET), Update (Http PATCH or PUT), Delete (HTTP Delete)
  CREATE ("C" in "CRUD")
# ENDPOINT --> create new record ... each must have unique date, date is Pkey
'''
@app.post('/utilities/water/daily/{newRecordDate}/{gallonsTotal}/', tags=["utilities", "daily", "water", "usage"])
async def create_daily_water_record(newRecordDate: str,
                                    gallonsTotal: float,
                                    gallonsHot: float
                                    ):

    newRecordDate = datetime.fromisoformat(newRecordDate).date()
    db_cursor = CONNECTION.cursor()
    db_cursor.execute(
        '''
        INSERT INTO "daily_water" (date, usage_type, total_gallons, total_hot)
        VALUES (%s, %s);
        ''', (newRecordDate, gallonsTotal, gallonsHot))
    message = (
        f"successfully executed INSERT(date {newRecordDate}, total_gallons {gallonsTotal}, total_hot {gallonsHot}")
    CONNECTION.commit(),
    return {"msg": [message]}

# READ ("R" in "CRUD")
# ENDPOINT Api Endpoint: Retrieves **all** records in daily_water Table
@app.get('/utilities/water/total/daily/all', tags=["utilities", "daily", "water", "usage"])
async def get_all_daily_water_values():
    db_cursor = CONNECTION.cursor()
    db_cursor.execute('SELECT * FROM "daily_water"')
    raw_result = db_cursor.fetchall()
    db_cursor.close()
    response_value = []
    for i in raw_result:
        print(i)
        daily_values = {}               # key/value pairs within JSON response
        daily_key = str(i[0])           # date ... key for a key/value pair within JSON
        daily_value = {}                # value values for key for a key/value pair
        daily_value["total_gallons"] = i[1]      # totalGallons
        daily_value["total_hot"] = i[2]
        daily_values[daily_key] = daily_value
        response_value.append(daily_values)
    return response_value

# UPDATE ("U" in "CRUD")
#ENDPOINT --> Update all water usage records via running Ryan's water calculations 
@app.put('/utilities/water/total/all/simulated/update/all', tags=["utilities", "daily", "water"])
async def update_all_daily_water_records_with_simulated_data():
    message=[]
    for i in water_calculations.calculate_water_usage():
        print(i[0])
        recDate = str(i[0])
        total_gallons = i[1]
        total_hot = i[2]
        db_cursor = CONNECTION.cursor()
        db_cursor.execute(
            '''
            INSERT INTO "daily_water" (date, total_gallons, total_hot)
            VALUES (%s, %s, %s);
            ''', (recDate, total_gallons, total_hot))
        message.append(
            f"successfully executed INSERT(date {recDate}, total_gallons {total_gallons}, total_hot {total_hot})")
        CONNECTION.commit()
        db_cursor.close()
    return {"msg": [message]}


# DELETE    ("D" in "CRUD")
# ENDPOINT Api Endpoint: Deletes a record, selected by date, in daily_water Table
@app.delete('utilities/water/total/daily/{dateToDelete}', tags=["utilities", "daily", "water"])
async def delete_daily_water_record_by_date(dateToDelete: str):
    db_cursor = CONNECTION.cursor()
    db_cursor.execute('DELETE FROM "daily_water" WHERE date = %s RETURNING *;', (dateToDelete,))
    message = (f"successfully deleted record for {dateToDelete}")
    CONNECTION.commit()
    return {"msg": [message]}


#                       Start of Electricity Section
# CRUD = Create (Http POST), Read(Http GET), Update (Http PATCH or PUT), Delete (HTTP Delete)
# CREATE ("C" in "CRUD"...CREATE READ UPDATE DELETE)
# ENDPOINT --> create new record ... each must have unique date, date is Pkey
@app.post('/utilities/electricity/{newRecordDate}/{kwh}/{cost}', tags=["utilities", "electricity", "daily"])
async def create_a_daily_electricity_record(newRecordDate: str, kwh: float, cost: float):
    db_cursor = CONNECTION.cursor()
    db_cursor.execute(
        '''
        INSERT INTO "daily_electricity" (date, kwh, cost)
        VALUES (%s, %s, %s);
        ''', (newRecordDate, kwh, cost))
    message = (
        f"successfully executed INSERT INTO \"daily_electricity\"(date {newRecordDate}, kwh {kwh}, cost {cost}")
    CONNECTION.commit(),
    return {"msg": [message]}


# ENDPOINT Api Endpoint: Retrieves **all** records in daily_electricity Table
@app.get('/utilities/electricity/daily/all', tags=["utilities", "electricity", "daily"])
async def get_all_daily_electricity_records():
    db_cursor = CONNECTION.cursor()
    db_cursor.execute('SELECT * FROM "daily_electricity"')
    raw_result = db_cursor.fetchall()
    db_cursor.close()
    response_value = []
    for i in raw_result:
        daily_values = {}               # key/value pairs within JSON response
        daily_key = str(i[0])           # date ... key for a key/value pair within JSON
        daily_value = {}                # value values for key for a key/value pair
        daily_value["kwh"] = i[1]      # kWh
        daily_value["cost"] = i[2]
        daily_values[daily_key] = daily_value
        response_value.append(daily_values)
    # the resulting daily_values for each iteration is appended to response_value
    return response_value


# ENDPOINT Api Endpoint: Deletes a record from daily_electricity using a date
@app.delete('/utilities/electricity/daily/{dateToDelete}', tags=["utilities", "electricity", "daily"])
async def delete_a_daily_electricity_record(dateToDelete: str):
    db_cursor = CONNECTION.cursor()
    db_cursor.execute('DELETE FROM "daily_electricity" WHERE date = %s RETURNING *;', (dateToDelete,))
    message = (f"successfully deleted record for {dateToDelete}")
    CONNECTION.commit()
    return {"msg": [message]}
