import pandas as pd

class Backtester:
    def __init__(self, data, initial_cash=100000):
        """
        data: pandas DataFrame with columns ['Date', 'Close']
        initial_cash: starting money
        """
        self.data = data.copy()
        self.cash = initial_cash
        self.position = 0  # number of shares
        self.portfolio_value = []

    def add_indicators(self, short_window=20, long_window=50):
        """Add moving averages"""
        self.data['MA_short'] = self.data['Close'].rolling(window=short_window).mean()
        self.data['MA_long'] = self.data['Close'].rolling(window=long_window).mean()

    def generate_signals(self):
        """Generate buy/sell signals"""
        self.data['Signal'] = 0

        self.data.loc[
            self.data['MA_short'] > self.data['MA_long'], 'Signal'
        ] = 1

        self.data.loc[
            self.data['MA_short'] < self.data['MA_long'], 'Signal'
        ] = -1

    def run_backtest(self):
        """Run the strategy"""
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            price = row['Close']
            signal = row['Signal']

            # BUY
            if signal == 1 and self.cash > 0:
                self.position = self.cash // price
                self.cash -= self.position * price

            # SELL
            elif signal == -1 and self.position > 0:
                self.cash += self.position * price
                self.position = 0

            total_value = self.cash + (self.position * price)
            self.portfolio_value.append(total_value)

        self.data['Portfolio_Value'] = self.portfolio_value

    def results(self):
        """Print final result"""
        final_value = self.data['Portfolio_Value'].iloc[-1]
        return {
            "Final Portfolio Value": final_value,
            "Total Return (%)": ((final_value / self.portfolio_value[0]) - 1) * 100
        }


# ------------------- USAGE -------------------

if __name__ == "__main__":
    # Example: load your own data here
    df = pd.read_csv("data.csv")  # must have 'Close' column

    bt = Backtester(df)

    bt.add_indicators(short_window=20, long_window=50)
    bt.generate_signals()
    bt.run_backtest()

    print(bt.results())
