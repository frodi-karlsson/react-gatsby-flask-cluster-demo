import React from "react";

export const TimeButtons: React.FC<{
  progressTime: (...args: number[]) => Promise<void>;
}> = ({ progressTime }) => {
  return (
    <div className="button-wrapper">
      <button className="button" onClick={() => progressTime(0, 0, 1)}>
        Progress Time (Minute)
      </button>
      <button
        className="button"
        onClick={() => progressTime(0, 1)}
      >
        Progress Time (Hour)
      </button>
      <button
        className="button"
        onClick={() => progressTime(1)}
      >
        Progress Time (Day)
      </button>
      <button
        className="button"
        onClick={() => progressTime(7)}
      >
        Progress Time (Week)
      </button>
      <button
        className="button"
        onClick={() => progressTime(30)}
      >
        Progress Time (Month)
      </button>
      <button
        className="button"
        onClick={() => progressTime(365)}
      >
        Progress Time (Year)
      </button>
    </div>
  );
};
