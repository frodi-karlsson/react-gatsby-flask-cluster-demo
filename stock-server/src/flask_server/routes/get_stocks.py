from flask import jsonify
from data_handler import handler
from pandas import Timestamp


def on_get_stocks(stock_handler: handler.Handler, ticker: str, start: str or None, end: str or None):
    """This describes the GET /api/stocks route.

    This function is called when the user wants to get the current state of the stocks.

    """
    if start is not None:
        start = Timestamp(start.replace("%20", " "))
    if end is not None:
        end = Timestamp(end.replace("%20", " "))
    return stock_handler.get_data(ticker, start, end).to_json(), 200
