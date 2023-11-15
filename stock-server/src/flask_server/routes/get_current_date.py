from data_handler import handler

def on_get_date(stock_handler: handler.Handler):
    """This describes the GET /api/date route.

    This function is called when the user wants to get the current date of the simulation.

    """
    print("on_get_date")
    return stock_handler.date.strftime("%Y-%m-%d %H:%M:%S"), 200
