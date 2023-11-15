from data_handler import handler


def on_get_portfolio(stock_handler: handler.Handler):
    """This describes the GET /api/portfolio route.

    This function is called when the user wants to get the portfolio of the user.

    """
    return stock_handler.portfolio.to_json(orient="records"), 200
