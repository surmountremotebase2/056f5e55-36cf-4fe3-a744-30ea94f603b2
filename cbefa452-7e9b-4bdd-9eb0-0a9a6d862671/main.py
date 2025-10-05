from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        # Define the assets to be traded; in this case, just TQQQ
        return ["TQQQ"]

    @property
    def interval(self):
        # Using a daily interval for the trading signals
        return "1day"

    def run(self, data):
        """
        This function is called to decide on the trading actions based on the defined interval.
        It calculates the RSI and makes a decision based on its value.
        """
        # Initialize the allocation to 0
        tqqq_stake = 0
        
        # Calculate the RSI for TQQQ
        rsi_values = RSI("TQQQ", data["ohlcv"], length=14)  # Commonly, a 14-day period is used for RSI calculations
      
        # Check if we have enough data to calculate RSI
        if rsi_values is not None and len(rsi_values) > 0:
            # Latest RSI value
            latest_rsi = rsi_values[-1]
            
            # Buy signal: RSI below 30 indicates potential undervaluation
            if latest_rsi < 30:
                tqqq_stake = 1  # Set allocation to 100%
                
            # Sell signal: RSI above 70 indicates potential overvaluation
            elif latest_rsi > 70:
                tqqq_stake = 0  # Set allocation to 0%

            # Else, maintain current position, not trading
            
        # Logging the decision (for inspection purposes)
        log(f"TQQQ Allocation: {tqqq_stake}, Latest RSI: {latest_rsi if 'latest_rsi' in locals() else 'N/A'}")
        
        # Return the target allocation
        return TargetAllocation({"TQQQ": tqqq_stake})