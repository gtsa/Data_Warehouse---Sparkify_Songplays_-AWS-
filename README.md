## Sparkify Data Warehouse (Amazon Web Services (AWS))

Wanting to analyze the data we've been collecting on songs and user activity on our new music streaming app, Sparkify's analytics team is particularly interested in understanding what songs users are listening to. 

Until recently we didn't have an easy way to query our data - which resides in a directory of JSON logs of user activity on the app, as well as a directory with JSON metadata on the songs in their app. We created intially a Postgres database with tables designed to optimize queries on song play analysis.

But given the need for scalability, ellasticity, and availability, we had to migrate on the cloud. 

To do so, and choosing Amazon Web Services (AWS), we follow the next steps:

- We create an S3 bucket to store our JSON files data
- We create a certain IAM user with privileges of access corresponding to a certain IAM role and Security Group
- We create a Redshift cluster which we use for our ETL process pipeline as well as the storage and query of our new schema
- We arrange our data in a star schema structure, building (using Python and SQL) the ETL pipeline from files in the S3 bucket into the tables/relations of our schema via two staging tables that act as a resorvior for the pre-transformed business data.

So, our schema consists of the following tables:

- **Staging Tables**
    
    1. staging_events - records the business data in the form we load them in bulk from the JSON files with the logs of user activity on the app
        - *event_id, artist_name, auth, user_first_name, user_gender, item_in_session, user_last_name, song_length, user_level, location, method, page,  registration, session_id, song_title, status, timestamp, user_agent, user_id*

    2. staging_songs - records the business data in the form we load them in bulk from the JSON files with the metadata on the songs in their app
        - *song_id, num_songs, artist_id, latitude, longitude, location, artist_name, title, duration, year*

- **Fact Table**
    
    3. songplays - records in log data associated with song plays i.e. records with page "NextSong"
        - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

- **Dimension Tables**
    
    4. users - users in the app
        - *user_id, first_name, last_name, gender, level*
    
    5. songs - songs in music database
        - *song_id, title, artist_id, year, duration*
    
    6. artists - artists in music database
        - *artist_id, name, location, latitude, longitude*
    
    7. time - timestamps of records in songplays broken down into specific units
        - *start_time, hour, day, week, month, year, weekday*
        
--------------------

#### Files in the respository

Our repository consists of the following files:

- **Python** files (***.py***)
    - ***sql_queries.py*** (contains all our sql queries that are imported into the following two files,
    - ***create_tables.py*** (drops and creates our tables. We run this file to reset our tables before each time we run our ETL scripts,
    - ***etl.py*** (reads and processes files from song_data and log_data and loads them into our tables
    
- **Configuration** file (***dwh.cfg***)
    - contains configuration information to access Redshift, IAM, and S3
---------------------

#### Instructions on how to run the scripts
For someone to build an image of our data warehouse (having already set appropriately their AWS  (S3, Redshift and IAM)), they must follow **serially** the following three steps:
   
   1. Lauch a command-line interface (terminal)
   
   2. Run ***create_tables.py***
   
    python create_tables.py
   
   3. Run ***etl.py***
   
    python create_tables.py

