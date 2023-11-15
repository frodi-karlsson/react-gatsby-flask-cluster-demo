from flask import jsonify
from data_handler import handler

def on_post_progress_time(stock_handler: handler.Handler, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    """This function is called when the user wants to progress the time."""
    print("on_post_progress_time")
    stock_handler.progress_time(
        days=int(days),
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds)
    )
    return stock_handler.date.strftime("%Y-%m-%d %H:%M:%S"), 200
