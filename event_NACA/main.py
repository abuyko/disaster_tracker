import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(user=os.getenv('user'),
                              password=os.getenv('password'),
                              host=os.getenv('host'),
                              port=os.getenv('port'),
                              database=os.getenv('database'))
cursor = connection.cursor()


def select_db(point=[], region_mile=0, start_datetime=None, end_datetime=None):
    distance = f""", (point({point[0]},{point[1]}) <@> events.event_coordinates) as distance""" if point else ""
    query = f"""select *{distance} from events"""
    if start_datetime:
        art = 'and' if 'where' in query else 'where'
        query += f""" {art}  event_date >= '{start_datetime}'"""
    if end_datetime:
        art = 'and' if 'where' in query else 'where'
        query += f""" {art}  event_date <= '{end_datetime}'"""
    if point and region_mile:
        query = f"""select * from ({query}) as tabl where distance <= {region_mile}"""
    return query


if __name__ == '__main__':
    kilometers=10000

    query=select_db(point=[0, 0], region_mile=kilometers * 0.621371, start_datetime='2021-12-13 18:00:00', end_datetime='2021-12-18 18:00:00')
    print(query)
    df = pd.read_sql_query(query, connection)
    print(df)