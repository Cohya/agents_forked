
import yfinance as yf
import pandas as pd
from pathlib import Path


def get_close_price(ticker_symbol) -> float:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d")
    return data["Close"].iloc[-1]


def update_my_stock_of_interest_prices(path_to_csv: Path = Path("stock_prices.csv")):
    df = pd.read_csv(path_to_csv)
    tickers_list = df['Ticker'].tolist()
    new_prices = []
    for ticker_symbole in tickers_list:
        price = get_close_price(ticker_symbole)
        print(f"The latest closing price for {ticker_symbole} is {price}")
        new_prices.append(price)

    df['Price'] = new_prices

    df.to_csv(path_to_csv, index=False)


if __name__ == "__main__":
   update_my_stock_of_interest_prices()