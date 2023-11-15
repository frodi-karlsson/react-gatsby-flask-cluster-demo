from flask import jsonify, request
from data_handler import handler

def on_post_sell(stock_handler: handler.Handler, ticker: str, amount: int):
    """This function is called when the user wants to buy a stock."""
    print("on_post_sell")
    res = stock_handler.sell(ticker, amount)
    if res[0]:
        return jsonify({"success": True }), 200
    else:
        return jsonify({"success": False, "reason": res[1]}), 400
