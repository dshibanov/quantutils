import os
import re
import pickle
from pprint import pprint
import pandas as pd

def load_tracks(folder):
    pattern = re.compile(r"(.+?)_(.+?)_(.+?)_(.+?)\.pkl")
    tracks = []

    for filename in os.listdir(folder):
        if filename.endswith(".pkl"):
            match = pattern.match(filename)
            if match:
                symbol, direction, amount, leverage = match.groups()
                filepath = os.path.join(folder, filename)
                with open(filepath, "rb") as f:
                    df = pickle.load(f)
                    # print(df)
                    # Min-Max Normalization (scaling to range 0 to 1)
                    df['order_book']['ask_normalized'] = (df['order_book']['ask'] - df['order_book']['ask'].min()) / (df['order_book']['ask'].max() - df['order_book']['ask'].min())
                    df['order_book']['bid_normalized'] = (df['order_book']['bid'] - df['order_book']['bid'].min()) / (df['order_book']['bid'].max() - df['order_book']['bid'].min())
                    df['pnl']['pnl_normalized'] = (df['pnl']['pnl'] - df['pnl']['pnl'].min()) / (df['pnl']['pnl'].max() - df['pnl']['pnl'].min())
                    df['merged'] = pd.merge(df['order_book'], df['pnl'], how='outer')
                    tracks.append(df)
    return tracks



def test_load_tracks():
    tracks = load_tracks('../../../datamart/tracks/')
    print(len(tracks))


if __name__ == "__main__":
    test_load_tracks()
