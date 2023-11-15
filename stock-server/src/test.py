from data_handler import handler
import pandas as pd

test_handler: handler.Handler = None

init_cash = 100000

failed_to_buy_error = RuntimeError("Failed to buy AAPL")


def setup_test():
    """This function sets up the test."""
    global test_handler
    test_handler = handler.Handler(
        # A random monday
        pd.Timestamp("2020-03-02 10:00:00"),
        init_cash,
    )


# buy tests
def test_buy_portfolio(handler: handler.Handler):
    """Tests if the portfolio is updated correctly on buy."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    portfolio = handler.portfolio
    quantity = portfolio.iloc[0]["quantity"]
    assert quantity == 10


def test_buy_portfolio_value(handler: handler.Handler):
    """Tests if the portfolio value is updated correctly on buy."""
    price = handler.get_price("AAPL")
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    assert handler.get_portfolio_value() == price * 10


def test_buy_history(handler: handler.Handler):
    """Tests if the history is updated correctly on buy."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    price = handler.get_price("AAPL")
    handler.progress_time(days=1)
    history = handler.history
    assert history.iloc[-1]["cash"] == init_cash - price * 10


buy_tests = [
    (test_buy_portfolio, "Is the portfolio updated correctly on buy?"),
    (test_buy_portfolio_value, "Is the portfolio value updated correctly on buy?"),
    (test_buy_history, "Is the history updated correctly on buy?"),
]


# sell tests
def test_sell_nonexistant(handler: handler.Handler):
    """Tests if selling a nonexistant stock fails."""
    res = handler.sell("AAPL", 10)
    assert not res[0]


def test_sell_more_than_owned(handler: handler.Handler):
    """Tests if selling more than is owned fails."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    res = handler.sell("AAPL", 20)
    assert not res[0]


def test_sell_portfolio(handler: handler.Handler):
    """Tests if the portfolio is updated correctly on sell."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    res = handler.sell("AAPL", 10)
    assert res[0]
    portfolio = handler.portfolio
    quantity = portfolio.iloc[0]["quantity"]
    assert quantity == 0


def test_sell_portfolio_value(handler: handler.Handler):
    """Tests if the portfolio value is updated correctly on sell."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    res = handler.sell("AAPL", 10)
    assert res[0]
    assert handler.get_portfolio_value() == 0


def test_sell_history(handler: handler.Handler):
    """Tests if the history is updated correctly on sell."""
    res = handler.buy("AAPL", 10)
    if not res[0]:
        raise failed_to_buy_error
    res = handler.sell("AAPL", 10)
    assert res[0]
    handler.progress_time(days=1)
    history = handler.history
    assert history.iloc[-1]["cash"] == init_cash


sell_tests = [
    (test_sell_nonexistant, "Is selling a nonexistant stock handled correctly?"),
    (test_sell_more_than_owned, "Is selling more than is owned handled correctly?"),
    (test_sell_portfolio, "Is the portfolio updated correctly on sell?"),
    (test_sell_portfolio_value, "Is the portfolio value updated correctly on sell?"),
    (test_sell_history, "Is the history updated correctly on sell?"),
]


# date tests
# these only test progress time and the date value
# as they are dependent on the other functions working
def test_date_progress_time_day(handler: handler.Handler):
    """Tests if the day is updated correctly."""
    handler.progress_time(days=1)
    assert handler.date == pd.Timestamp("2020-03-03 10:00:00")


def test_date_progress_time_hour(handler: handler.Handler):
    """Tests if the hour is updated correctly."""
    handler.progress_time(hours=1)
    assert handler.date == pd.Timestamp("2020-03-02 11:00:00")


def test_date_progress_time_minute(handler: handler.Handler):
    """Tests if the minute is updated correctly."""
    handler.progress_time(minutes=1)
    assert handler.date == pd.Timestamp("2020-03-02 10:01:00")


def test_date_progress_time_second(handler: handler.Handler):
    """Tests if the second is updated correctly."""
    handler.progress_time(seconds=1)
    assert handler.date == pd.Timestamp("2020-03-02 10:00:01")


def test_date_progress_time_all(handler: handler.Handler):
    """Tests if the time is updated correctly."""
    handler.progress_time(days=1, hours=1, minutes=1, seconds=1)
    assert handler.date == pd.Timestamp("2020-03-03 11:01:01")


date_tests = [
    (test_date_progress_time_day, "Is the day updated correctly?"),
    (test_date_progress_time_hour, "Is the hour updated correctly?"),
    (test_date_progress_time_minute, "Is the minute updated correctly?"),
    (test_date_progress_time_second, "Is the second updated correctly?"),
    (test_date_progress_time_all, "Is the time updated correctly?"),
]


def print_red(text: str):
    """This function prints the given text in red."""
    print(f"\033[91m{text}\033[0m")


def print_green(text: str):
    """This function prints the given text in green."""
    print(f"\033[92m{text}\033[0m")


# reset tests
def test_reset(handler: handler.Handler):
    """Tests if the handler is reset correctly."""
    handler.buy("AAPL", 10)
    handler.reset()
    assert handler.date == pd.Timestamp("2021-03-01 10:00:00")
    assert handler.cash == init_cash
    assert handler.portfolio.empty
    assert handler.history.empty


reset_tests = [
    (test_reset, "Is the handler reset correctly?"),
]


# test setup
def run_tests():
    """This function runs all the tests."""
    failed = []
    for test in buy_tests + sell_tests + date_tests + reset_tests:
        setup_test()
        print(f"Running test: {test[1]}")
        try:
            test[0](test_handler)
            print_green("Test passed")
        except Exception as e:
            print_red(f"Test failed! {e}")
            failed.append(test[1])
    if len(failed) > 0:
        print("The following tests failed:")
        for fail in failed:
            print_red(f"  {fail}")
        raise RuntimeError("Tests failed")
    else:
        print_green("All tests passed")
        exit(0)


if __name__ == "__main__":
    run_tests()
