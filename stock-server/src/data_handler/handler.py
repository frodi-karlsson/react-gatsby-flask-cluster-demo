import yfinance as yf
import pandas as pd
from numpy import float64


class Handler:
    """Handles parsing historical stock data"""

    date: pd.Timestamp
    initial_cash: float

    def __init__(self, date: pd.Timestamp, initial_cash: float):
        if not isinstance(date, pd.Timestamp):
            if isinstance(date, str):
                date = pd.to_datetime(date)
            else:
                raise TypeError(f"date must be of type pd.Timestamp, not {type(date)}")
        if not isinstance(initial_cash, float):
            if isinstance(initial_cash, int):
                initial_cash = float(initial_cash)
            else:
                raise TypeError(
                    f"initial_cash must be of type float, not {type(initial_cash)}"
                )

        self.date = date
        self.initial_cash = initial_cash
        self.portfolio = pd.DataFrame(columns=["ticker", "quantity", "date"])
        self.cash = initial_cash
        self.history = pd.DataFrame(columns=["date", "cash", "portfolio_value"])

    def get_date_with_time(
        self,
        date: pd.Timestamp,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ):
        """Increments the date by the given number of days, hours, minutes, and seconds and returns the new date as well as if it is a new day"""
        new_date = date + pd.Timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        return (
            new_date,
            new_date.day != date.day,
        )

    def get_data(
        self, ticker: str, start: pd.Timestamp or None, end: pd.Timestamp or None
    ) -> pd.DataFrame:
        """Gets the historical data for the given ticker"""
        interval = "1m"
        today = pd.Timestamp.today()
        if start is None:
            start = self.get_date_with_time(self.date)[0]
        if end is None:
            end = self.get_date_with_time(self.date, days=1)[0]
        # We can only get 7 days of 1m data at a time, and want to avoid getting 1d data if possible
        # We also don't want to try to get data from the future or too far in the past
        if abs((end - start).days) > 7 or end > today or (today - end).days >= 30:
            interval = "1d"
        data: pd.DataFrame = yf.download(
            ticker,
            interval=interval,
            start=start,
            end=end,
            progress=False,
        )
        return data

    def get_price(self, ticker: str) -> float or None:
        """Gets the price of the given ticker on the given date"""
        date = self.get_date_with_time(self.date)[0]
        data = self.get_data(ticker, date, None)
        if data.empty:
            return None
        return data["Close"].iloc[0]

    def buy(self, ticker: str, quantity: int) -> (bool, str or None):
        """Buys the given quantity of the given ticker on the given date"""
        price = self.get_price(ticker)
        quantity = float64(quantity)
        if price is None:
            return (False, "Ticker not found")
        if price * quantity > self.cash:
            return (False, "Not enough cash")
        self.cash -= price * quantity
        df = pd.DataFrame(
            [
                {
                    "ticker": ticker,
                    "quantity": quantity,
                    "date": self.date,
                }
            ]
        )
        if self.portfolio.empty:
            self.portfolio = df
            return (True, None)
        elif ticker in self.portfolio["ticker"].values:
            self.portfolio.loc[
                self.portfolio["ticker"] == ticker, "quantity"
            ] += quantity
            return (True, None)
        else:
            self.portfolio = pd.concat(
                [
                    self.portfolio,
                    df,
                ],
                ignore_index=True,
            )
            return (True, None)

    def sell(self, ticker: str, quantity: int) -> (bool, str or None):
        """Sells the given quantity of the given ticker on the given date"""
        if ticker not in self.portfolio["ticker"].values:
            return (False, "Ticker not found in portfolio")
        price = self.get_price(ticker)
        quantity = float64(quantity)
        if price is None:
            return (False, "Ticker not found. The market may be closed.")
        if (
            quantity
            > (self.portfolio.loc[self.portfolio["ticker"] == ticker, "quantity"].iloc[0])
        ):
            return (False, "Not enough shares")
        self.cash += price * quantity
        self.portfolio.loc[
            self.portfolio["ticker"] == ticker, "quantity"
        ] -= quantity
        return (True, None)

    def set_date(self, date: pd.Timestamp) -> None:
        """Sets the date"""
        self.date = date

    def on_next_day(self) -> None:
        """Updates history and portfolio for the day"""
        df = pd.DataFrame(
            [
                {
                    "date": self.date,
                    "cash": self.cash,
                    "portfolio_value": self.get_portfolio_value(),
                },
            ]
        )
        if self.history.empty:
            self.history = df
        else:
            self.history = pd.concat(
                [
                    self.history,
                    df,
                ],
                ignore_index=True,
            )

    def progress_time(
        self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0
    ) -> None:
        """Progresses the time by the given number of days, hours, minutes, and seconds"""
        new_date, new_day = self.get_date_with_time(
            self.date, days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        if new_day:
            self.on_next_day()
        self.date = new_date

    def get_portfolio_value(self) -> float:
        """Gets the value of the portfolio"""
        portfolio_value = 0
        for index, row in self.portfolio.iterrows():
            quantity = row["quantity"]
            ticker = row["ticker"]
            price = self.get_price(ticker)
            if price is None:
                continue
            portfolio_value += quantity * price
        return portfolio_value

    def reset(self) -> None:
        """Resets the handler"""
        self.__init__("2021-03-01 10:00:00", self.initial_cash)

    def __str__(self) -> str:
        return f"Handler:\ndate={self.date}\ninitial_cash={self.initial_cash}\nportfolio=\n{self.portfolio.to_string()}\ncash={self.cash}\nhistory=\n{self.history.to_string()}"
