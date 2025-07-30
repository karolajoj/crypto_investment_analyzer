# Crypto Investment Analyzer

A tool to analyze cryptocurrency investment strategies using historical data, visualizations, and optimization.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/karolajoj/crypto_investment_analyzer.git
   cd crypto_investment_analyzer
   ```

2. Set up a virtual environment:
   ```bash
   py -3.12 -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with example parameters:
```bash
python src\main.py --currency BTC --timeframe 1h --start-date 2025-01-01 --lookback 30d --percentiles 25,50,75
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.