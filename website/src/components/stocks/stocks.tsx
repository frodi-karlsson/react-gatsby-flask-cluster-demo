import * as React from "react";
import { Portfolio, StockHandler } from "./StockHandler";
import { TimeButtons } from "./partials/time-buttons";
import { PortfolioDiv } from "./partials/portfolio";
import { UpdateWatchedDiv } from "./partials/update-watched-div";
import { StockDiv } from "./partials/stock-div";
import "../../styles/stocks.css";

export type StockStateType = {
        cash: number;
        date: string;
        portfolio: Portfolio[];
        portfolioValue: number;
        watchedStocks: string[];
        symbol: string;
        priceMap: { [ticker: string]: number };
        loading: boolean;
}

export class StockView extends React.Component<
  {},
  StockStateType
> {
  stockHandler: StockHandler;

  constructor(props: any) {
    super(props);
    this.state = {
      cash: 0,
      date: "",
      portfolio: [],
      portfolioValue: 0,
      watchedStocks: [],
      symbol: "",
      priceMap: {},
      loading: true,
    };
    this.stockHandler = new StockHandler();
    this.update();
  }
  async updateWatched(symbol: string): Promise<void> {
    const stock = await this.stockHandler.getStock(symbol).catch((e) => {
      console.error("error", e);
      return undefined;
    });
    if (!stock) {
      return;
    }
    const lastValue = stock.Close[stock.Close.length - 1];
    this.setState((state) => ({
      priceMap: { ...state.priceMap, [symbol]: lastValue },
      watchedStocks: [...new Set(state.watchedStocks.concat(symbol))],
    }));
  }

  async buyStock(symbol: string, quantity: number): Promise<boolean> {
    const res = await this.stockHandler.buyStock(symbol, quantity);
    if (res) {
      await this.update();
    }
    return res;
  }

  async sellStock(symbol: string, quantity: number): Promise<boolean> {
    const res = await this.stockHandler.sellStock(symbol, quantity);
    if (res) {
      await this.update();
    }
    return res;
  }

  setSymbol(cb: (state: StockStateType) => string): void {
    this.setState((state) => ({
        symbol: cb(state),
    }));
  }

  setWatchedStocks(cb: (state: StockStateType) => string[]): Promise<void> {
    this.setState((state) => ({
        watchedStocks: cb(state),
    }));
    return this.update();
  }

  async progressTime(...args: number[]): Promise<void> {
    await this.stockHandler.progressTime(...args);
    await this.update();
  }

  async reset(): Promise<void> {
    await this.stockHandler.reset();
    await this.update();
  }

  async update(): Promise<void> {
    this.setState({ loading: true });
    try {
      const cash = await this.stockHandler.getCash().catch((e) => {
        console.error("error", e);
        return 0;
      });
      const date = await this.stockHandler.getDate().catch((e) => {
        console.error("error", e);
        return "";
      });
      const portfolio = await this.stockHandler.getPortfolio().catch((e) => {
        console.error("error", e);
        return [];
      });
      const portfolioValue = await this.stockHandler
        .getPortfolioValue()
        .catch((e) => {
          console.error("error", e);
          return 0;
        });
      this.setState({ cash, date, portfolio, portfolioValue });
      if (portfolio?.length > 0) {
          const promise = portfolio
            .map((stock) => stock.ticker)
            .concat(this.state.watchedStocks)
            .map(this.updateWatched.bind(this));
          await Promise.all(promise);
      }
    } catch (e) {
      console.error("error", e);
    }
    this.setState({ loading: false });
  }

  componentDidMount(): void {
    this.update();
  }


  render(): JSX.Element {
    return (
      <div className="stock-view-wrapper">
        <div className="stock-view-header">Stocks</div>
        <div className="stock-view-content">
          <div
            className="loading"
            style={{ display: this.state.loading ? "flex" : "none" }}
          >
            Loading...
          </div>
          <TimeButtons progressTime={this.progressTime.bind(this)} />
          <PortfolioDiv state={this.state} reset={this.reset.bind(this)} />
          <UpdateWatchedDiv
            state={this.state}
            setSymbol={this.setSymbol.bind(this)}
            setWatchedStocks={this.setWatchedStocks.bind(this)}
          />
          <StockDiv
            buyStock={this.buyStock.bind(this)}
            sellStock={this.sellStock.bind(this)}
            state={this.state}
          />
        </div>
      </div>
    );
  }
}
