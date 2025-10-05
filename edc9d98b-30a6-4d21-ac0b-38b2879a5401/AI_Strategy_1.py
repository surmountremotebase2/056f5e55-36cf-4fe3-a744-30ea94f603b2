from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class MomentumTradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TQQQ", "SPY"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily data to determine momentum
        return "1day"

    @property
    def data(self):
        # No additional data sources are required for this strategy
        return []

    def run(self, data):
        # Initialize the allocation dictionary
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        for ticker in self.tickers:
            # Calculate the MACD for each ticker
            macd_values = MACD(ticker, data["ohlcv"], fast=12, slow=26)

            if macd_values is not None:
                # Use the MACD line and signal line to determine the momentum
                macd_line = macd_values['MACD']
                signal_line = macd_values['signal']
                
                # Check the latest available MACD and signal values to determine the trading signal
                if len(macd_line) > 0 and len(signal_line) > 0:
                    latest_macd = macd_line[-1]
                    latest_signal = signal_line[-1]
                    
                    # If the MACD line crosses above the signal line, allocate to the asset
                    if latest_macd > latest_signal:
                        allocation_dict[ticker] = 0.5  # Allocate 50% to this asset
                    else:
                        # No allocation if the MACD line is below the signal line
                        allocation_dict[ticker] = 0
                        
            else:
                log(f"MACD calculation failed for {ticker}, skipping allocation.")

        # Return the target allocation
        return TargetAllocation(allocation_dict)

# Create an instance of the strategy
trading_strategy = MomentumTradingStrategy()

# Print out the strategy's properties to verify setup (as an example, actual strategy running will depend on the Surmount framework to call run method with data)
print(f"Assets: {trading_strategy.assets}")
print(f"Interval: {trading_strategy.interval}")
print(f"Data Requirements: {trading_strategy.data}")