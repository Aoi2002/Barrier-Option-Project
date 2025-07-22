# get_usdjpy_data.py
import yfinance as yf
import pandas as pd

def download_usdjpy(start="2022-01-01", end="2023-12-31", filename="data/usdjpy_fx_data.csv"):
    """
    Download USD/JPY FX data from Yahoo Finance and save as CSV
    """
    df = yf.download("JPY=X", start=start, end=end)
    df = df[["Open", "High", "Low", "Close"]]
    df.rename(columns={"Close": "USDJPY"}, inplace=True)
    df.dropna(inplace=True)
    df.to_csv(filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    download_usdjpy()
