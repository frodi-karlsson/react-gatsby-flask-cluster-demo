import React from "react";
import { StockStateType } from "../stocks";

export const PortfolioDiv: React.FC<{
  state: StockStateType;
  reset: () => Promise<void>;
}> = ({ state, reset }) => {
  return (
    <div className="portfolio-wrapper">
      <div className="stock-view-header">
        Portfolio
        <br />
        Cash: ${state.cash.toFixed(2)}
        <br />
        Date: {state.date}
        <br />
        Value: ${state.portfolioValue.toFixed(2)}
        <button className="button" onClick={() => reset()}>
          Reset
        </button>
      </div>
      <div className="table">
        <div className="table-header">
          <div className="table-header-cell">Symbol</div>
          <div className="table-header-cell">Shares</div>
          <div className="table-header-cell">Value</div>
        </div>
        {state.portfolio.map((stock) => (
          <div className="table-row" key={stock.ticker}>
            <div className="table-cell">{stock.ticker}</div>
            <div className="table-cell">{stock.quantity}</div>
            <div className="table-cell">
              {state.priceMap[stock.ticker]
                ? (state.priceMap[stock.ticker] * stock.quantity).toFixed(2)
                : 0}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
