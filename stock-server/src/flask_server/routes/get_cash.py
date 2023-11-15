from data_handler import handler
from flask import jsonify


def on_get_cash(stock_handler: handler.Handler):
    """This describes the GET /api/cash route.

    This function is called when the user wants to get the cash of the user.

    """
    return jsonify({"cash": stock_handler.cash}), 200
