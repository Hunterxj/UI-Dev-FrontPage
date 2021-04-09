<h1> Readme: ButlerAPI </h1>
<h2> By Will Watts </h2>

# Table of Contents

[Part One: ButlerAPI](#pt1)

1. [General Information: Overview of ButlerAPI and Its Code](#pt1ch1)
2. [FAQ](#pt1ch2)
3. [Modules Used](#pt1ch3)
4. [How To Use This API](#pt1ch4)
5. [Variable Name Glossary](#pt1ch5)

[Part Two: UI](#pt2)

1.[General Information: Overview of UI and Its Code](#pt2ch1)





## 1.) General Information: Overview of ButlerAPI and Its Code <a name=pt1ch1></a>

**Author of this API and its documentation: Will Watts**
**Project Created For: CSA-499, Group 5, Spring 2021 at UAB**
**MIT License.**

<h3> Purpose and Basic Functionality </h3>

ButlerAPI is designed to perform tasks and retrieve data required 
for an IoT "Smart Home" device with functionality similar to a typical thermostat, but with the added ability to view data and data visualizations that give insights into utility usages and costs. This device can also toggle the power on or off for supported devices.

<h3> Code Overview and Technologies Used </h3>

> ButlerAPI is written in **Python 3.9.1** Modules are managed by Pip. It utilizes several open-source modules. 
Some of the more notable modules used include:

> - **FastAPI**: this is a tool similar to Flask, but with more modern features and an emphasis on JSON/REST. FastAPI's name comes from its fast performance. It also provides features such as the inclusion of automatically generated Swagger and Redoc documentation.

> -**Pydantic**: this allows for an intuitive approach to modeling objects in Python.

> -**Psycopg2**: this functions as a database driver that connects Python projects to a PostgreSQL database. Psycopg2 handles database connections and operations.

ButlerAPI uses the REST API design pattern. REST is an intuitive and popular way to go about API design, and it allows for a hassle-free experience when it comes to
actually utilizing the API in a project. FastAPI was chosen instead of the more commonly used Flask due to its excellent performance, out-of-the-box JSON support, and excellent API documentation features.

ButlerAPI connects to the remote PostgreSQL database via the Psycopg2 module, and utilizes 
Pydantic's intuitive way of modeling data objects.

In a nutshell, this API is designed to be as intuitive as possible. 
The API endpoints have URLs that are designed to be easily memorable, 
and the code itself has been written and revised with the goal of it 
being easily and immediately understood by anyone with minimal hassle. 
Another goal of this API is to keep the code as short as possible, 
which further simplifies maintenance and future modifications or feature additions. 
API records are returned in JSON format.

Pip was chosen over Anaconda to handle the environment and packages after careful consideration. 
Anaconda would have been more complicated for other developers to work with, and Anaconda has fewer packages. 
Pip also allows the use of requirements .txt file (via pip --freze terminal commands). Using a requirements text file simplifies the process of sharing packages and downloading them with less steps involved for the API author 
and his users, since it greatly reduces the hassle of maintaining a Python environment and preventing misconfigurations across separate computers.

## 2.) FAQ <a name=pt1ch2></a>

**Q: What is REST? (related terms: RESTful web services/REST API/ other acronyms with 'REST' in them)**

REST is an acronym for **Re**presentational **S**tate **T**ransfer.

> A: REST API design is a design pattern for APIs. It is probably the most popular design pattern for APIs today, but I'm not sure who is actually measuring that.
> Before REST, there was SOAP (Simple Object Access Protocol). SOAP is not very fun to use, and it typically 
returns XML, which is definitely not fun to use for web API purposes.

REST APIs are well explained in the link below.

<a href=https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/> Understanding and Using REST APIs<a/>

\*As a general rule, REST APIs tend to JSON data as a response. JSON is a convenient format to work with.

- **Q: Why use REST though?**

> A: REST is easy. Plus we can make really simple URLs for fetching items from the database. For example:

    # returns ALL weather records on the database's WeatherData table
    ...../weather-records/

    #returns ONLY the weather records within the date range between startDate and endDate
    #......../weather-records/startDate/endDate

    # NOTE: the date range endpoint is not yet implemented as of today. 
It's the next thing going in. The ALL weather records endpoint is in.

## 3.) Modules Used <a name=pt1ch3></a>

<h3> API Framework: **FastAPI** </h3>

\*FastAPI is a fairly new API framework for Python.

- Quickly gaining popularity as an alternative to Flask.
- Has more modern features than Flask, and is supposedly faster.
- Supports JSON out of the box.
- OpenAPI documentation provided via Swagger and Redoc (both included with generation and UI -- minimal if any setup needed).
- So far, my tests indicate this is way better than Flask, and implementing features like API documentation (ex: Swagger) is much much simpler.
- Built on Pydantic, which helps with models.
- As of this writing, I'm still learning the ropes of this particular framework. It's much beefier than Flask.

<h3>Database Driver / Connector: **psycopg2** </h3>

> <a href=https://pypi.org/project/psycopg2/>psycopg2 : Project Page on PyPi.org </a>

\*Lets Python talk to our PostgreSQL database.

*db_cursor and CONNECTION both come from here.
*handles connection parameters.

## 4.) How To Use This API <a name=pt1ch4></a>



Coming soon, whenever API functionality is in near-finished state.






## 5.) Variable Name Glossary <a name=pt1ch5></a>

**<h3>CONNECTION</h3>**

> This is an instance of psycopg2.connect

This sets up your database connection.

    '''
    Connection Parameters for database
    '''
    CONNECTION = psycopg2.CONNECTION()
    #Connection Parameters for database
    CONNECTION = psycopg2.connect(
    host = "164.111.161.243",
    dbname = "Team5DB",
    user = "Team5",
    password = "team5",
    sslmode = "disable")

**<h3>db_cursor </h3>**

> This is an instance of psycopg2.cursor

_Note: Documentation and tutorials often name their instance of this as "cur."_

<a href=https://www.psycopg.org/docs/usage.html> How To Use</a>

This is an important one.
db_cursor is an instance of psycopg2.cursor.

> This functions basically as a controller for database interactions.

> The cursor controls what is selected and acted upon in the database.

    db_cursor = CONNECTION.cursor()

> _Above: as of this writing, this is the code in main.py that declares the db_cursor. 
CONNECTION is explained in the next entry in this glossary._

1.) **Open cursor (see example below).**

    cursor = connection.cursor()

**2.) Execute desired command.**

    cursor.execute("select \* from WeatherData)

> This is the syntax we use to make SQL queries using psycopg2.

**3.)Always close cursor when done.**

    cursor.close()

> Seriously, always close the cursor! This prevents leaks.

#Model For Weather Record (this is one entry as a model)
'''





<h1>Part Two: UI <a name=pt2></a></h1>

## General Overview of UI Project and its code. <a name="pt2ch1"></a>
This section is coming soon.

