import os
import json
import psycopg2
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(user=os.getenv('user'),
                              password=os.getenv('password'),
                              host=os.getenv('host'),
                              port=os.getenv('port'),
                              database=os.getenv('database'))
cursor = connection.cursor()


def get_events(days):
    payload = {
        'days': days
    }
    response = requests.get('https://eonet.gsfc.nasa.gov/api/v3/events', params=payload)
    if response.status_code == 200:
        return response.json()['events']
    return []


def add_db(event):
    for geometry in event['geometry']:
        info = {
            'event_id': event['id'],
            'event_title': event['title'],
            'event_description': event['description'],
            'event_link': event['link'],
            'event_closed': event['closed'],
            'event_categories': json.dumps(event['categories']),
            'event_magnitudeValue': geometry['magnitudeValue'],
            'event_magnitudeUnit': geometry['magnitudeUnit'],
            'event_date': datetime.strptime(geometry['date'], "%Y-%m-%dT%H:%M:%SZ"),
            'event_type': geometry['type'],
            'event_coordinates': f"({geometry['coordinates'][0]},{geometry['coordinates'][1]})"
        }
        query = f"""select * from events where event_id='{info['event_id']}' and event_date='{info['event_date']}'"""
        df = pd.read_sql_query(query, connection)
        if df.empty:
            sql_insert_query = """
             INSERT INTO events(event_id, event_title, event_description, event_link, event_closed, event_categories, 
             event_magnitudeValue, event_magnitudeUnit, event_date, event_type, event_coordinates) 
             VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""
            result = cursor.executemany(sql_insert_query, [[info[key] for key in info]])
    connection.commit()


if __name__ == '__main__':
    days = 365
    from pprint import pprint
    for event in tqdm(get_events(days)):
        pprint(event)
        # add_db(event)
        break
