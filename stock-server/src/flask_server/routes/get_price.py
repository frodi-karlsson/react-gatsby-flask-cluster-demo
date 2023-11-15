from data_handler import handler


def on_get_price(stock_handler: handler.Handler, stock: str):
    """This describes the GET /api/price route.

    This function is called when the user wants to get the price of a stock.

    """
    return stock_handler.get_price(stock), 200
