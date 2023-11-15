from data_handler import handler

def on_delete_reset(handler: handler.Handler):
    """This describes the DELETE /api/reset route.

    This function is called when the user wants to reset the server.

    """
    handler.reset()
    return "Reset", 200
