from flask import Flask, request, Blueprint, Response
from flask_cors import CORS
from flask_server.routes import (
    get_stocks,
    post_buy,
    get_current_date,
    post_progress_time,
    get_portfolio,
    get_portfolio_value,
    get_cash,
    get_history,
    get_price,
    post_sell,
    delete_reset,
)
from data_handler import handler


def _init_cors(_app: Flask):
    """This function initializes the CORS for the Flask server."""

    CORS(_app, resources={r"/api/*": {
        "origins": "*",
        "supports_credentials": True,
        "allow_headers": "*",
        "expose_headers": "*",
        "methods": "*",
    }})

    @_app.before_request
    def handle_options():
        res = Response()
        res.headers.add("Access-Control-Allow-Origin", "*")
        res.headers.add("X-Content-Type-Options", "nosniff")
        res.headers.add("Access-Control-Allow-Headers", "*")
        res.headers.add("Access-Control-Allow-Methods", "*")
        if request.method == "OPTIONS":
            return res


def _init_api_routes(_app: Flask, stock_handler: handler.Handler):
    """This function initializes the routes for a blueprint and registers poit with the Flask server."""

    bp = Blueprint("api", __name__, url_prefix="/api")

    @bp.get("/date")
    def on_get_date():
        return get_current_date.on_get_date(stock_handler)

    @bp.post(
        "/date/progress_time",
        defaults={"days": 0, "hours": 0, "minutes": 0, "seconds": 0},
    )
    @bp.post(
        "/date/progress_time/<days>", defaults={"hours": 0, "minutes": 0, "seconds": 0}
    )
    @bp.post(
        "/date/progress_time/<days>/<hours>", defaults={"minutes": 0, "seconds": 0}
    )
    @bp.post("/date/progress_time/<days>/<hours>/<minutes>", defaults={"seconds": 0})
    @bp.post("/date/progress_time/<days>/<hours>/<minutes>/<seconds>")
    def on_post_progress_time(days: int, hours: int, minutes: int, seconds: int):
        return post_progress_time.on_post_progress_time(
            stock_handler, days, hours, minutes, seconds
        )

    @bp.post("/buy/<ticker>/<amount>")
    def on_post_buy(ticker: str, amount: int):
        return post_buy.on_post_buy(stock_handler, ticker, amount)

    @bp.post("/sell/<ticker>/<amount>")
    def on_post_sell(ticker: str, amount: int):
        return post_sell.on_post_sell(stock_handler, ticker, amount)

    @bp.get("/stocks/<ticker>", defaults={"start": None, "end": None})
    @bp.get("/stocks/<ticker>/<start>/", defaults={"end": None})
    @bp.get("/stocks/<ticker>/<start>/<end>")
    def on_get_stocks(ticker: str, start: str or None, end: str or None):
        return get_stocks.on_get_stocks(stock_handler, ticker, start, end)

    @bp.get("/price/<ticker>")
    def on_get_price(ticker: str):
        return get_price.on_get_price(stock_handler, ticker)

    @bp.get("/portfolio")
    def on_get_portfolio():
        return get_portfolio.on_get_portfolio(stock_handler)

    @bp.get("/history")
    def on_get_history():
        return get_history.on_get_history(stock_handler)

    @bp.get("/portfolio/value")
    def on_get_portfolio_value():
        return get_portfolio_value.on_get_portfolio_value(stock_handler)

    @bp.get("/cash")
    def on_get_cash():
        return get_cash.on_get_cash(stock_handler)

    @bp.delete("/reset")
    def reset():
        return delete_reset.on_delete_reset(stock_handler)

    @bp.after_request
    def after_request(response):
        print(f"Sent response: {response.status_code}, {response.data}")
        return response

    _app.register_blueprint(bp)


def _init_error_handlers(_app: Flask):
    """This function initializes the error handlers for the Flask server."""

    @_app.errorhandler(404)
    def page_not_found(e):
        return "404: Page not found", 404

    @_app.errorhandler(Exception)
    def handle_exception(e):
        print(e)
        return "500: Internal server error", 500


def init(_app: Flask, stock_handler: handler.Handler):
    """This function initializes the Flask server"""
    # This function initializes the Flask server
    _init_cors(_app)
    _init_api_routes(_app, stock_handler)
    _init_error_handlers(_app)


def start(stock_handler: handler.Handler):
    """This function initializes and starts the Flask server."""
    _app = Flask(__name__)
    _app.app_context().push()
    init(_app, stock_handler)
    _app.run(debug=True, host="0.0.0.0", port=5000)
