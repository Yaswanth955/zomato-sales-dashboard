import pandas as pd
import random
from datetime import datetime
import time
import os

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai']
items = ['Pizza', 'Burger', 'Biryani', 'Pasta', 'Sandwich']

def generate_row():
    return {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'city': random.choice(cities),
        'item': random.choice(items),
        'quantity': random.randint(1, 5),
        'price': random.randint(100, 500)
    }

def simulate_data(file='sales.csv', interval=5):
    if not os.path.exists(file):
        pd.DataFrame(columns=['timestamp', 'city', 'item', 'quantity', 'price']).to_csv(file, index=False)

    while True:
        df = pd.DataFrame([generate_row()])
        df.to_csv(file, mode='a', header=False, index=False)
        print(f"New sale added at {df['timestamp'].iloc[0]}")
        time.sleep(interval)

if __name__ == "__main__":
    simulate_data()
