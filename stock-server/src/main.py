from flask_server import server
from data_handler import handler
from dotenv import load_dotenv
from pandas import Timestamp
import os

load_dotenv()

handler = handler.Handler(
    date=Timestamp("2021-03-01 10:00:00"),
    initial_cash=100000,
)

# The main function for this project simply starts the Flask server
def main():
    server.start(handler)


if __name__ == "__main__":
    main()
