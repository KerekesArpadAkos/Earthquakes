import requests
import pandas as pd
from datetime import datetime, timezone
import schedule
import time
from send_email_alert import send_email_alert
from send_sms_alert import send_sms_alert

# API URL for real-time earthquake data
API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# Store IDs of earthquakes that have already been alerted
alerted_earthquakes = set()

# Function to fetch real-time earthquake data
def fetch_earthquake_data():
    print("Fetching earthquake data...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        features = data['features']

        records = []
        for feature in features:
            properties = feature['properties']
            geometry = feature['geometry']
            record = {
                'id': feature['id'],
                'time': datetime.fromtimestamp(properties['time'] / 1000, tz=timezone.utc),
                'latitude': geometry['coordinates'][1],
                'longitude': geometry['coordinates'][0],
                'depth': geometry['coordinates'][2],
                'mag': properties['mag'],
                'place': properties['place'],
                'type': properties['type']
            }
            records.append(record)

        df = pd.DataFrame(records)
        print(f"Fetched {len(df)} earthquake records.")
        return df
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# Function to process and analyze data
def process_earthquake_data(df):
    global alerted_earthquakes
    print("Processing earthquake data...")
    try:
        # Example rule: Trigger alert if magnitude >= 2
        alert_df = df[(df['mag'] >= 2) & (~df['id'].isin(alerted_earthquakes))]
        if not alert_df.empty:
            print(f"ALERT: {len(alert_df)} significant earthquakes detected!")
            for _, row in alert_df.iterrows():
                alert_message = f"Time: {row['time']}\nLocation: {row['place']}\nMagnitude: {row['mag']}"
                print(alert_message)
                send_email_alert("Earthquake Alert", alert_message, "akosmlyrics@gmail.com")
                send_sms_alert(alert_message)
                alerted_earthquakes.add(row['id'])
        else:
            print("No significant earthquakes detected.")
    except Exception as e:
        print(f"Failed to process data: {e}")

# Function to run the real-time monitoring
def run_monitoring():
    print("Running monitoring...")
    df = fetch_earthquake_data()
    if not df.empty:
        process_earthquake_data(df)
    print("Monitoring completed.\n")

# Schedule the monitoring to run every minute
schedule.every(1).minutes.do(run_monitoring)

# Run the scheduler
print("Starting real-time earthquake monitoring system...")
while True:
    schedule.run_pending()
    time.sleep(1)
