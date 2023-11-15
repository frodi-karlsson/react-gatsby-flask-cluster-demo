import * as React from "react"
import type { PageProps } from "gatsby"
import { StockView } from "../components/stocks/stocks";
import "../styles/index.css"

console.log("Inside index.tsx");

const IndexPage: React.FC<PageProps> = () => {
  return (
    <StockView />
  )
}

export default IndexPage

export const Head = () => (
  <head>
    <title>Stocks</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>
);
