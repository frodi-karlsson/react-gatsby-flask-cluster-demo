import axios, { AxiosInstance, AxiosResponse, AxiosError } from "axios";
import axiosRetry from "axios-retry";

axiosRetry(axios, {
  retries: 3,
  retryCondition: (error) => {
    console.log(error);
    return error.response?.status === 500;
  },
  shouldResetTimeout: true,
});

export interface Stock {
  Date: string[];
  Open: number[];
  High: number[];
  Low: number[];
  Close: number[];
  "Adj Close": number[];
  Volume: number[];
}

export interface Portfolio {
  ticker: string;
  quantity: number;
  date: string;
}

export interface History {
  date: string;
  cash: number;
  portfolio_value: number;
}

/**
 * A class to handle interactions with the API
 * @class APIHandler
 *
 * @property {string} apiURL - The URL of the API
 */
class APIHandler {
  apiURL: string = "http://kubernetes.docker.internal/api";

  constructor() {
    console.log("apiURL", this.apiURL);
  }

  api: AxiosInstance = axios.create({
    baseURL: this.apiURL,
    url: "/",
    timeout: 3000,
  });

  async getDate(): Promise<string> {
    return this.api.get("date").then((res) => res.data);
  }

  async progressTime(
    days: number = 0,
    hours: number = 0,
    minutes: number = 0,
    seconds: number = 0
  ): Promise<string> {
    return this.api.post(
      `date/progress_time/${days}/${hours}/${minutes}/${seconds}`
    );
  }

  async reset(): Promise<void> {
    return this.api.delete("reset");
  }

  async buyStock(ticker: string, quantity: number): Promise<boolean> {
    return this.api
      .post(`buy/${ticker}/${quantity}`)
      .then((res) => res.data.success)
      .catch((err: AxiosError) => {
        if (err.response?.status === 400) {
          return false;
        }
      });
  }

  async sellStock(ticker: string, quantity: number): Promise<boolean> {
    return this.api
      .post(`sell/${ticker}/${quantity}`)
      .then((res) => res.data.success)
      .catch((err: AxiosError) => {
        if (err.response?.status === 400) {
          return false;
        }
      });
  }

  async getStock(
    ticker: string,
    startDate: string | null,
    endDate: string | null
  ): Promise<Stock> {
    console.log("getting stock from api");
    const getStockFromResponse = (res: AxiosResponse): Stock => {
      const stock: Record<keyof Stock, Record<string, any>> = res.data;
      const newObj: Stock = {
        Close: Object.values(stock.Close),
        Date: Object.keys(stock.Close).map((dateInMs) => {
          const date = new Date(parseInt(dateInMs));
          return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
        }),
        High: Object.values(stock.High),
        Low: Object.values(stock.Low),
        Open: Object.values(stock.Open),
        "Adj Close": Object.values(stock["Adj Close"]),
        Volume: Object.values(stock.Volume),
      };
      console.log("newObj", newObj);
      return newObj;
    };

    if (!startDate && endDate) {
      return {
        Close: [],
        Date: [],
        High: [],
        Low: [],
        Open: [],
        "Adj Close": [],
        Volume: [],
      };
    } else if (startDate && !endDate) {
      return this.api
        .get(`stocks/${ticker}/${startDate}`)
        .then((res) => getStockFromResponse(res));
    } else if (!startDate && !endDate) {
      return this.api
        .get(`stocks/${ticker}`)
        .then((res) => getStockFromResponse(res));
    } else {
      return this.api
        .get(`stocks/${ticker}/${startDate}/${endDate}`)
        .then((res) => getStockFromResponse(res));
    }
  }

  async getPrice(ticker: string): Promise<number> {
    console.log(ticker);
    return this.api.get(`price/${ticker}`).then((res) => res.data);
  }

  async getPortfolio(): Promise<Portfolio[]> {
    return this.api.get("portfolio").then((res) => res.data);
  }

  async getPortfolioValue(): Promise<number> {
    return this.api.get("portfolio/value").then((res) => res.data.value);
  }

  async getCash(): Promise<number> {
    console.log("getting cash from api");
    return this.api.get("cash").then((res) => {
      console.log(res);
      return res.data.cash;
    });
  }

  async getHistory(): Promise<History[]> {
    return this.api.get("history");
  }
}

/**
 * The wrapper for stock data and API calls for use in the react app
 * @class StockHandler
 */
export class StockHandler {
  apiHandler: APIHandler = new APIHandler();

  /**
   * Get the current date in the simulation
   * @returns {Promise<string>} The current date
   */
  async getDate(): Promise<string> {
    return this.apiHandler.getDate();
  }

  /**
   * Reset the simulation
   * @returns {Promise<void>}
   */
  async reset(): Promise<void> {
    return this.apiHandler.reset();
  }

  /**
   * Progress the time in the simulation
   * @param {number} days - The number of days to progress
   * @param {number} hours - The number of hours to progress
   * @param {number} minutes - The number of minutes to progress
   * @param {number} seconds - The number of seconds to progress
   * @returns {Promise<string>} The new date
   */
  async progressTime(
    days: number = 0,
    hours: number = 0,
    minutes: number = 0,
    seconds: number = 0
  ): Promise<string> {
    return this.apiHandler.progressTime(days, hours, minutes, seconds);
  }

  /**
   * Buy a stock
   * @param {string} ticker - The ticker of the stock to buy
   * @param {number} quantity - The number of shares to buy
   * @returns {Promise<boolean>} Whether the purchase was successful
   */
  async buyStock(ticker: string, quantity: number): Promise<boolean> {
    return this.apiHandler.buyStock(ticker, quantity);
  }

  /**
   * Sell a stock
   * @param {string} ticker - The ticker of the stock to sell
   * @param {number} quantity - The number of shares to sell
   * @returns {Promise<boolean>} Whether the sale was successful
   */
  async sellStock(ticker: string, quantity: number): Promise<boolean> {
    return this.apiHandler.sellStock(ticker, quantity);
  }

  /**
   * Get the stock data for a given ticker
   * @param {string} ticker - The ticker of the stock to get data for
   * @param {string} startDate - The start date of the data
   * @param {string} endDate - The end date of the data
   * @returns {Promise<Stock[]>} The stock data
   */
  async getStock(
    ticker: string,
    startDate: string | null = null,
    endDate: string | null = null
  ): Promise<Stock> {
    return this.apiHandler.getStock(ticker, startDate, endDate);
  }

  /**
   * Get the price of a stock
   * @param {string} ticker - The ticker of the stock to get the price of
   * @returns {Promise<number>} The price of the stock
   */
  async getPrice(ticker: string): Promise<number> {
    return this.apiHandler.getPrice(ticker);
  }

  /**
   * Get the portfolio
   * @returns {Promise<Portfolio[]>} The portfolio
   */
  async getPortfolio(): Promise<Portfolio[]> {
    return this.apiHandler.getPortfolio();
  }

  /**
   * Get the total value of all portfolio holdings
   * @returns {Promise<number>} The portfolio value
   */
  async getPortfolioValue(): Promise<number> {
    return this.apiHandler.getPortfolioValue();
  }

  /**
   * Get the current cash
   * @returns {Promise<number>} The cash
   */
  async getCash(): Promise<number> {
    console.log("getting cash");
    return this.apiHandler.getCash().then((res) => {
      console.log(res);
      return res;
    });
  }

  /**
   * Get the history of the simulation
   * @returns {Promise<History[]>} The history
   */
  async getHistory(): Promise<History[]> {
    return this.apiHandler.getHistory();
  }
}
