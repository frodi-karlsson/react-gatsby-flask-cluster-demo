import React from "react";
import { StockStateType } from "../stocks";

export const StockDiv: React.FC<{
  buyStock: (ticker: string, quantity: number) => Promise<boolean>;
  sellStock: (ticker: string, quantity: number) => Promise<boolean>;
  state: StockStateType;
}> = ({ buyStock, sellStock, state }) => {
  return (
    <div className="table">
      <div className="table-header">
        <div className="table-header-cell">Symbol</div>
        <div className="table-header-cell">Price</div>
        <div className="table-header-cell">Actions</div>
      </div>
      {state.watchedStocks.map((stock, index) => (
        <div className="table-row" key={stock}>
          <div className="table-cell">{stock}</div>
          <div className="table-cell">
            {state.priceMap[stock] ? state.priceMap[stock].toFixed(2) : 0}
          </div>
          <div className="table-cell">
            <div className="input-wrapper">
              <input
                type="number"
                min="1"
                max="1000"
                defaultValue="1"
                className="input"
                id={`input-${index}`}
              />
              <button
                className="button"
                onClick={() => {
                  const quantity = parseInt(
                    (
                      document.getElementById(
                        `input-${index}`
                      ) as HTMLInputElement
                    ).value
                  );
                  buyStock(stock, quantity).then((res) => {
                    if (!res) {
                      alert("Could not buy stock. Maybe the market is closed or you don't have enough cash?");
                    }
                  });
                }}
              >
                Buy
              </button>
              <button
                className="button"
                onClick={() => {
                  const quantity = parseInt(
                    (
                      document.getElementById(
                        `input-${index}`
                      ) as HTMLInputElement
                    ).value
                  );
                  sellStock(stock, quantity).then((res) => {
                    if (!res) {
                      alert(
                        "Could not sell stock. Maybe the market is closed or you don't have enough shares?"
                      );
                    }
                  });
                }}
              >
                Sell
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
