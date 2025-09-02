import requests
import logging
from datetime import datetime, timedelta
from technical_indicators import TechnicalIndicators

class CryptoScanner:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.indicators = TechnicalIndicators()
        
    def get_coin_id(self, symbol):
        """Get CoinGecko coin ID from symbol"""
        try:
            url = f"{self.base_url}/coins/list"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            coins = response.json()
            symbol_lower = symbol.lower()
            
            # First try exact match
            for coin in coins:
                if coin['symbol'].lower() == symbol_lower:
                    return coin['id']
            
            return None
        except Exception as e:
            logging.error(f"Error getting coin ID for {symbol}: {str(e)}")
            return None
    
    def get_historical_data(self, coin_id, days=100):
        """Get historical price data for a coin"""
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            prices = data['prices']
            
            # Convert to list of closing prices
            closing_prices = [price[1] for price in prices]
            
            return closing_prices
        except Exception as e:
            logging.error(f"Error getting historical data for {coin_id}: {str(e)}")
            return None
    
    def get_current_price(self, coin_id):
        """Get current price for a coin"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if coin_id in data:
                return {
                    'price': data[coin_id]['usd'],
                    'change_24h': data[coin_id].get('usd_24h_change', 0)
                }
            
            return None
        except Exception as e:
            logging.error(f"Error getting current price for {coin_id}: {str(e)}")
            return None
    
    def analyze_coin(self, symbol, rsi_period=14):
        """Analyze a single cryptocurrency"""
        try:
            # Get coin ID
            coin_id = self.get_coin_id(symbol)
            if not coin_id:
                logging.warning(f"Could not find coin ID for symbol: {symbol}")
                return None
            
            # Get historical data
            prices = self.get_historical_data(coin_id)
            if not prices or len(prices) < 30:
                logging.warning(f"Insufficient price data for {symbol}")
                return None
            
            # Get current price
            current_data = self.get_current_price(coin_id)
            if not current_data:
                logging.warning(f"Could not get current price for {symbol}")
                return None
            
            # Calculate indicators
            rsi = self.indicators.calculate_rsi(prices, period=rsi_period)
            macd_data = self.indicators.calculate_macd(prices)
            
            if rsi is None or macd_data is None:
                logging.warning(f"Could not calculate indicators for {symbol}")
                return None
            
            # Determine signals
            rsi_signal = self.get_rsi_signal(rsi)
            macd_signal = self.get_macd_signal(macd_data)
            combined_signal = self.get_combined_signal(rsi_signal, macd_signal)
            
            return {
                'symbol': symbol.upper(),
                'coin_id': coin_id,
                'price': current_data['price'],
                'change_24h': current_data['change_24h'],
                'rsi': round(rsi, 2),
                'rsi_signal': rsi_signal,
                'macd_line': round(macd_data['macd_line'], 6),
                'signal_line': round(macd_data['signal_line'], 6),
                'histogram': round(macd_data['histogram'], 6),
                'macd_signal': macd_signal,
                'combined_signal': combined_signal,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logging.error(f"Error analyzing {symbol}: {str(e)}")
            return None
    
    def get_rsi_signal(self, rsi):
        """Determine RSI signal"""
        if rsi > 70:
            return 'Overbought'
        elif rsi < 30:
            return 'Oversold'
        else:
            return 'Neutral'
    
    def get_macd_signal(self, macd_data):
        """Determine MACD signal"""
        macd_line = macd_data['macd_line']
        signal_line = macd_data['signal_line']
        histogram = macd_data['histogram']
        
        if macd_line > signal_line and histogram > 0:
            return 'Bullish'
        elif macd_line < signal_line and histogram < 0:
            return 'Bearish'
        else:
            return 'Neutral'
    
    def get_combined_signal(self, rsi_signal, macd_signal):
        """Determine combined signal strength"""
        # Strong signals when both indicators align
        if rsi_signal == 'Oversold' and macd_signal == 'Bullish':
            return 'Strong Buy'
        elif rsi_signal == 'Overbought' and macd_signal == 'Bearish':
            return 'Strong Sell'
        elif rsi_signal in ['Oversold'] and macd_signal != 'Bearish':
            return 'Buy'
        elif rsi_signal in ['Overbought'] and macd_signal != 'Bullish':
            return 'Sell'
        elif macd_signal == 'Bullish' and rsi_signal != 'Overbought':
            return 'Buy'
        elif macd_signal == 'Bearish' and rsi_signal != 'Oversold':
            return 'Sell'
        else:
            return 'Hold'
    
    def scan_multiple_coins(self, symbols, rsi_period=14):
        """Scan multiple cryptocurrencies"""
        results = []
        
        for symbol in symbols:
            try:
                result = self.analyze_coin(symbol, rsi_period)
                if result:
                    results.append(result)
                else:
                    logging.warning(f"Failed to analyze {symbol}")
            except Exception as e:
                logging.error(f"Error scanning {symbol}: {str(e)}")
                continue
        
        # Sort by combined signal strength and RSI
        signal_priority = {
            'Strong Buy': 1,
            'Buy': 2,
            'Hold': 3,
            'Sell': 4,
            'Strong Sell': 5
        }
        
        results.sort(key=lambda x: (signal_priority.get(x['combined_signal'], 6), x['rsi']))
        
        return results
