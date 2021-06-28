import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load in bulk (using COPY) business
    data into the staging tables
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Populates fact and dimension tables with data selected from staging tables
    (only from NextSong page and if necessary,
    lightly manipulated by sql functions or selected0
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Parses .cfg file
    - Establishes connection with AWS using details and credentials of the .cfg file 
    - Load data into the staging tables
    - Populates fact and dimension tables
    - Finally, closes the connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()