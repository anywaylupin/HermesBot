import ccxt from "ccxt";
import delay from "delay";
import moment from "moment";

const binance = new ccxt.binance({
  apiKey: "cxNFNrRvFjpkwf6f7TGz1IXVVgUP9gPd9vPiCwUq6bXsR2wgaf1luyO3yznmhPse",
  secret: "jAfUkbtU8BQhvKLKS03UqBASP8GUU9PszyVRTXSLainzgImawd8xWg6tU2K2KcMR",
});

binance.setSandboxMode(true);

const tick = async () => {
  const prices = await binance.fetchOHLCV("BTC/USDT", "1m", undefined, 5);
  const bPrices = prices.map((price) => ({
    timestamp: moment(price[0]).format(),
    open: price[1],
    high: price[2],
    low: price[3],
    close: price[4],
    volume: price[5],
  }));

  const averagePrice = bPrices.reduce((acc, price) => acc + price.close, 0) / 5;
  const lastPrice = bPrices[bPrices.length - 1].close;

  console.log(
    bPrices.map((p) => p.close),
    averagePrice,
    lastPrice
  );

  const direction = lastPrice > averagePrice ? "sell" : "buy";
  const TRADE_SIZE = 100;

  const quantity = TRADE_SIZE / lastPrice;
  const order = await binance.createMarketOrder("BTC/USDT", direction, quantity);

  console.log(`Average Price: ${averagePrice}`);
  console.log(`Last Price: ${lastPrice}`);
  console.log(`${moment().format()}: ${direction} ${quantity} BTC at  ${lastPrice}`);
  console.log(order);

  printBalance(lastPrice);
};

const printBalance = async (btcPrice) => {
  const balance = await binance.fetchBalance();
  const total = balance.total;
  console.log(`Balance: BTC ${total.BTC}, USDT: ${total.USDT}`);
  console.log(`Total USDT: ${(total.BTC - 1) * btcPrice + total.USDT} \n`);
  return balance;
};

const main = async () => {
  while (true) {
    await tick();
    await delay(2000);
  }
};

main();
