# Crypto RSI & MACD Scanner

## Overview

A Flask-based web application that provides technical analysis of cryptocurrencies using RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence) indicators. The application allows users to input cryptocurrency symbols and analyze their technical indicators to aid in trading decisions. It integrates with the CoinGecko API to fetch real-time and historical cryptocurrency data, then applies mathematical calculations to generate technical analysis insights.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Styling**: Custom CSS with dark theme support and gradient designs
- **JavaScript**: Vanilla JavaScript for form validation, input formatting, and interactive features
- **UI Framework**: Bootstrap 5 with Font Awesome icons and Chart.js for data visualization
- **Theme**: Dark theme implementation with consistent color variables

### Backend Architecture
- **Web Framework**: Flask with RESTful route structure
- **Application Structure**: Modular design separating concerns into distinct components:
  - `app.py`: Main Flask application and route handlers
  - `crypto_scanner.py`: Core business logic for cryptocurrency data retrieval
  - `technical_indicators.py`: Mathematical calculations for technical analysis
  - `main.py`: Application entry point
- **Data Processing**: NumPy-based calculations for technical indicators
- **Error Handling**: Comprehensive exception handling with user-friendly flash messages
- **Logging**: Built-in Python logging for debugging and monitoring

### Data Storage Solutions
- **Session Management**: Flask sessions with configurable secret key
- **Data Flow**: Stateless request-response model with no persistent data storage
- **Caching Strategy**: No explicit caching implemented (relies on API response times)

### API Integration Pattern
- **External API**: CoinGecko API v3 for cryptocurrency data
- **Data Retrieval**: Historical price data fetched for technical analysis calculations
- **Symbol Resolution**: Dynamic coin ID lookup from cryptocurrency symbols
- **Rate Limiting**: Basic timeout handling (10-second timeout per request)

## External Dependencies

### Third-Party APIs
- **CoinGecko API**: Primary data source for cryptocurrency prices and historical data
  - Endpoint: `https://api.coingecko.com/api/v3`
  - Used for: Coin listings, historical price data, market charts
  - Rate limits: Public API with standard rate limiting

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome 6.4.0**: Icon library for enhanced user interface
- **Chart.js**: Data visualization library for potential chart implementations

### Python Dependencies
- **Flask**: Web framework for application structure
- **requests**: HTTP library for API communication
- **numpy**: Mathematical operations for technical indicator calculations
- **logging**: Built-in Python module for application monitoring

### Development Dependencies
- **Python 3.x**: Runtime environment
- **Flask development server**: Local development and testing