import numpy as np
import logging

class TechnicalIndicators:
    def __init__(self):
        pass
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index (RSI)"""
        try:
            if len(prices) < period + 1:
                return None
            
            prices = np.array(prices)
            deltas = np.diff(prices)
            
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # Calculate initial average gain and loss
            avg_gain = np.mean(gains[:period])
            avg_loss = np.mean(losses[:period])
            
            # Calculate smoothed averages
            for i in range(period, len(deltas)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                return 100
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logging.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        try:
            prices = np.array(prices)
            if len(prices) < period:
                return None
            
            multiplier = 2 / (period + 1)
            ema = prices[0]  # Start with first price
            
            for price in prices[1:]:
                ema = (price * multiplier) + (ema * (1 - multiplier))
            
            return ema
            
        except Exception as e:
            logging.error(f"Error calculating EMA: {str(e)}")
            return None
    
    def calculate_macd(self, prices, fast_period=12, slow_period=26, signal_period=9):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            if len(prices) < slow_period + signal_period:
                return None
            
            prices = np.array(prices)
            
            # Calculate EMAs
            fast_ema = self.calculate_ema_series(prices, fast_period)
            slow_ema = self.calculate_ema_series(prices, slow_period)
            
            if fast_ema is None or slow_ema is None:
                return None
            
            # Align arrays by taking the minimum length
            min_length = min(len(fast_ema), len(slow_ema))
            fast_ema_aligned = fast_ema[-min_length:]
            slow_ema_aligned = slow_ema[-min_length:]
            
            # Calculate MACD line
            macd_line = fast_ema_aligned[-1] - slow_ema_aligned[-1]
            
            # Calculate MACD values for signal line
            macd_values = fast_ema_aligned - slow_ema_aligned
            
            # Calculate signal line (EMA of MACD)
            signal_line = self.calculate_ema(macd_values, signal_period)
            
            if signal_line is None:
                return None
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            return {
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': histogram
            }
            
        except Exception as e:
            logging.error(f"Error calculating MACD: {str(e)}")
            return None
    
    def calculate_ema_series(self, prices, period):
        """Calculate EMA series for all prices"""
        try:
            if len(prices) < period:
                return None
            
            prices = np.array(prices)
            multiplier = 2 / (period + 1)
            
            # Initialize with simple moving average for first EMA
            ema_values = [np.mean(prices[:period])]
            
            # Calculate EMA for remaining prices
            for i in range(period, len(prices)):
                ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
                ema_values.append(ema)
            
            return np.array(ema_values)
            
        except Exception as e:
            logging.error(f"Error calculating EMA series: {str(e)}")
            return None
    
    def calculate_sma(self, prices, period):
        """Calculate Simple Moving Average"""
        try:
            if len(prices) < period:
                return None
            
            prices = np.array(prices)
            return np.mean(prices[-period:])
            
        except Exception as e:
            logging.error(f"Error calculating SMA: {str(e)}")
            return None
