import os
import logging
from flask import Flask, render_template, request, jsonify, flash
from crypto_scanner import CryptoScanner

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-crypto-scanner")

# Initialize crypto scanner
crypto_scanner = CryptoScanner()

@app.route('/')
def index():
    """Main page with combined RSI and MACD analysis"""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_crypto():
    """Scan cryptocurrencies with RSI and MACD analysis"""
    try:
        symbols = request.form.get('symbols', '').strip()
        if not symbols:
            flash('Please enter at least one cryptocurrency symbol', 'error')
            return render_template('index.html')
        
        # Parse symbols (comma-separated)
        symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
        
        # Get RSI period from form (default 14)
        rsi_period = int(request.form.get('rsi_period', 14))
        
        # Scan cryptocurrencies
        results = crypto_scanner.scan_multiple_coins(symbol_list, rsi_period=rsi_period)
        
        if not results:
            flash('No data found for the provided symbols. Please check symbol names.', 'warning')
            return render_template('index.html')
        
        return render_template('index.html', results=results, symbols=symbols, rsi_period=rsi_period)
        
    except ValueError as e:
        flash(f'Invalid input: {str(e)}', 'error')
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error scanning crypto: {str(e)}")
        flash('An error occurred while scanning. Please try again.', 'error')
        return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def api_scan_crypto():
    """API endpoint for JavaScript-based scanning"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        rsi_period = data.get('rsi_period', 14)
        
        if not symbols:
            return jsonify({'error': 'No symbols provided'}), 400
        
        results = crypto_scanner.scan_multiple_coins(symbols, rsi_period=rsi_period)
        return jsonify({'results': results})
        
    except Exception as e:
        logging.error(f"API scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/popular')
def popular_coins():
    """Get analysis for popular cryptocurrencies"""
    try:
        popular_symbols = ['BTC', 'ETH', 'LINK', 'XRP', 'SOL']
        results = crypto_scanner.scan_multiple_coins(popular_symbols)
        return render_template('index.html', results=results, symbols=','.join(popular_symbols), is_popular=True)
    except Exception as e:
        logging.error(f"Error getting popular coins: {str(e)}")
        flash('An error occurred while fetching popular coins.', 'error')
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
