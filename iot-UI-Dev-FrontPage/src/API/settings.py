settings={}
settings["METEOSTAT_API_KEY"] = "W1Iocfp15ZJC7mvGN9AI4eHHnQkEeDs1"
settings["WEATHER_STATION"] = "72228"

settings["TAGS_METADATA"] = [
    {
        "name": "utilities",
        "description": "Records and operations for water and electric usage.",
    },

    {
        "name": "water",
        "description": "Records and operations for water and electric usage.",
    },

    {
        "name": "electricity",
        "description": "Records and operations for water and electric usage.",
    },

    {
        "name": "hourly",
        "description": "These functions deal with hourly records that are stored in the database. "
                       "Records stored in database all originate from sensor data with the exception of weather data, "
                       "which is fetched from the external Meteostat API."
                       "Meteostat API data is provided in metric units (degrees C, KM, KM/H, mm, etc)"
    },
    {
        "name": "daily",
        "description": "These functions deal with daily records that are stored in the database. "
                       "Records stored in database all originate from sensor data with the exception of weather data, "
                       "which is fetched from the external Meteostat API."
                        "Meteostat API data is in metric units (degrees C, KM, KM/H, mm, etc)"
                        
    },

    {
        "name": "weather",
        "description": "Daily weather records and operations associated with them."
                        "Important Note: Meteostat API data is in metric units (degrees C, KM, KM/H, mm, etc)"

    
    },

    {
        "name": "openapi",
        "description": "These endpoints are related to API documentation that follows the OpenAPI standard (for example, this swagger endpoint you are currently viewing).",
        
    },

    {
        "name": "usage",
        "description": "These endpoints pertain to utility usage records.",
        
    },

    {
        "name": "cost",
        "description": "These endpoints pertain to utility expense records.",
        
    },

]

settings["DB_PARAMS"] = {
    'database': 'Team5DB',
    'user': 'Team5',
    'password': 'team5',
    'host': '164.111.161.243',
    'port': '5432'
}

