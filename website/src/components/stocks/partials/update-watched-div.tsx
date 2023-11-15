import React from "react";
import { StockStateType } from "../stocks";

export const UpdateWatchedDiv: React.FC<{
    state: StockStateType;
    setSymbol: (cb: (state: StockStateType) => string) => void;
    setWatchedStocks: (cb: (state: StockStateType) => string[]) => void;
}> = ({ state, setSymbol, setWatchedStocks }) => {
  return (
    <div className="input-wrapper" id="update-watched">
      <input
        className="input"
        type="text"
        placeholder="Symbol"
        value={state.symbol}
        onChange={(e) => setSymbol(() => e.target.value.toUpperCase())}
      />
      <button
        className="button"
        onClick={() => {
          if (state.watchedStocks.find((s) => s === state.symbol)) {
            alert("Already watching that stock!");
          } else {
            setWatchedStocks((state => [...state.watchedStocks, state.symbol]));
          }
        }}
      >
        Watch
      </button>
    </div>
  );
};
