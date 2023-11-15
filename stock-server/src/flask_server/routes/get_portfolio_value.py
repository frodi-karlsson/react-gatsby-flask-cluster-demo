from data_handler import handler
from flask import jsonify


def on_get_portfolio_value(stock_handler: handler.Handler):
    """This describes the GET /api/portfolio/value route.

    This function is called when the user wants to get the value of the portfolio of the user.

    """
    return jsonify({"value": stock_handler.get_portfolio_value()}), 200
