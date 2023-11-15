from data_handler import handler


def on_get_history(stock_handler: handler.Handler):
    """This describes the GET /api/history route.

    This function is called when the user wants to get the hisstory of the user.

    """
    return stock_handler.history.to_json(orient="records"), 200
