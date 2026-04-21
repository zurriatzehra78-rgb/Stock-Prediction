
```markdown
# 📈 PSX Stock Predictor - Professional Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.17+-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)

**Real-time Pakistan Stock Exchange (PSX) Analysis Tool with Technical Indicators, Portfolio Tracking, and Price Predictions**

</div>

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Architecture](#-project-architecture)
- [Supported Stocks](#-supported-stocks)
- [Troubleshooting](#-troubleshooting)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**PSX Stock Predictor** is a professional-grade financial analysis application designed specifically for the Pakistan Stock Exchange. It provides real-time data analysis, technical indicators, portfolio management with tax calculations, and price predictions to help investors make informed decisions.

### Problem Statement
Pakistani retail investors lack access to:
- Real-time PSX analysis tools
- Integrated profit/loss calculators with tax implications
- Professional technical indicators for local stocks
- Portfolio tracking with brokerage fees

### Solution
This application solves these problems by providing a unified platform with:
- Real-time data fetching from PSX via yFinance
- 10+ technical indicators
- Built-in tax calculator (15% CGT + 5% fees)
- Interactive charts and predictions

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📊 Real-time Data | Live prices from PSX via Yahoo Finance | ✅ |
| 📈 Candlestick Charts | Interactive OHLC charts with MA overlays | ✅ |
| 💼 Portfolio Tracker | Track investments, profits, and taxes | ✅ |
| 🎯 Price Predictions | 5-month linear regression forecasts | ✅ |
| 🔍 Technical Indicators | RSI, MA20, MA50, Bollinger Bands | ✅ |
| 📉 Support/Resistance | Automatic level detection | ✅ |
| 🕯️ Pattern Recognition | Double bottom, Head & Shoulders | ✅ |
| 📊 Volume Analysis | Unusual volume detection | ✅ |
| 💰 Tax Calculator | 15% Capital Gains + 5% fees | ✅ |
| 📱 Responsive UI | Works on desktop & tablet | ✅ |

### Advanced Analytics
- **Trend Strength Detection** (ADX-based)
- **Buy/Sell Signal Generation** with confidence scoring
- **Volatility Calculation** (Annualized)
- **Risk Metrics** (Beta)

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Streamlit | 1.28+ | UI Framework |
| Plotly | 5.17+ | Interactive Charts |
| Custom CSS | - | Styling & Gradients |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core Logic |
| Pandas | 2.0+ | Data Manipulation |
| NumPy | 1.24+ | Mathematical Computations |
| yFinance | 0.2+ | Market Data API |

### Analytics (Custom Built)
- Linear Regression (Predictions)
- RSI Calculator
- ADX Trend Strength
- Support/Resistance Clustering
- Pattern Recognition (Double Bottom, Head & Shoulders)
- Volume Profile Analysis

---

## 📸 Screenshots

*(Place your screenshots in a `screenshots/` folder)*

| Dashboard | Candlestick Chart |
|-----------|-------------------|
| ![Dashboard](screenshots/dashboard.png) | ![Candlestick](screenshots/candlestick.png) |

| Portfolio Analysis | Technical Indicators |
|-------------------|---------------------|
| ![Portfolio](screenshots/portfolio.png) | ![Indicators](screenshots/indicators.png) |

| Price Predictions | Trading Signals |
|------------------|-----------------|
| ![Predictions](screenshots/predictions.png) | ![Signals](screenshots/signals.png) |

---

## 💻 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (optional)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/psx-stock-predictor.git
cd psx-stock-predictor
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
python -c "import streamlit, yfinance, pandas, plotly; print('All packages installed successfully!')"
```

#### 5. Run the Application
```bash
# Method 1: Direct streamlit
streamlit run index.py

# Method 2: Using launcher
python launch.py
```

#### 6. Open Browser
- Navigate to `http://localhost:8501`
- You should see the PSX Stock Predictor interface

---

## 📖 Usage Guide

### Basic Usage

#### 1. Select a Stock
```
Sidebar → Stock Selection → Choose from dropdown
Optional: Filter by sector (Banking, Cement, etc.)
```

#### 2. Load Data
```
Click "Analyze Stock" button
Wait 2-3 seconds for real-time data
```

#### 3. View Analysis
Navigate through tabs:
- **Price Chart**: Historical prices + volume
- **Technical Analysis**: RSI, MAs, Bollinger Bands
- **Predictions**: 5-month forecast
- **Advanced Signals**: Buy/Sell recommendations

### Portfolio Tracking Setup

#### Enter Your Investment Details:
```
1. Purchase Price per Share (PKR) → Example: 118.50
2. Total Purchase Price (PKR) → Example: 500,000
3. Required Profit (%) → Example: 20% target return
4. Tax Rate (%) → Default: 15% (Pakistan CGT)
5. Utilities Rate (%) → Default: 5% (Brokerage + Fees)
```

#### Understanding the Output:

**Portfolio Status Box Shows:**
```
PORTFOLIO STATUS

Purchase Details:
- Purchase Price per Share: PKR 100.00
- Total Investment: PKR 500,000
- Number of Shares: 5,000

Current Status (Before Tax):
- Current Price: PKR 118.50
- Profit/Loss per Share: +18.50 (+18.5%)
- Total Profit/Loss: +92,500
- Current Portfolio Value: 592,500

After Tax & Utilities (15% Tax + 5% Fees):
- Net Profit per Share: +14.80 (+14.8%)
- Net Total Profit: +74,000

Recommendation: HOLD - Profit Not Yet at Target
```

### Reading Trading Signals

| Signal | Confidence | Action |
|--------|------------|--------|
| STRONG BUY | 55%+ | Accumulate |
| CAUTIOUS BUY | 35-55% | Buy on dips |
| HOLD | 20-35% | Wait |
| NEUTRAL | Below 20% | No action |
| CAUTIOUS SELL | 35-55% | Reduce exposure |
| STRONG SELL | 55%+ | Exit position |

---

## 🏗️ Project Architecture

### Directory Structure
```
psx-stock-predictor/
│
├── index.py                 # Main application (600+ lines)
├── launch.py               # Launcher script
├── requirements.txt        # Dependencies
├── config.toml            # Streamlit configuration
├── .gitignore             # Git ignore rules
│
└── screenshots/           # Documentation images
    ├── dashboard.png
    ├── candlestick.png
    └── ...
```

### Class Architecture

```python
PSXStockPredictor (Main Class)
├── __init__()
│   └── psx_stocks (12 stocks database)
│
├── fetch_stock_data()
│   ├── yfinance API calls
│   └── fallback to simulated data
│
├── calculate_technical_indicators()
│   ├── RSI calculation
│   ├── Moving averages
│   └── Bollinger Bands
│
├── predict_future()
│   ├── Linear regression
│   └── Confidence intervals
│
└── generate_sample_data()
    └── Monte Carlo simulation

AdvancedTrendAnalyzer (Signals Class)
├── find_support_resistance()
├── detect_trend_strength()
├── identify_chart_patterns()
└── generate_signal()

### Data Flow

User Input → Sidebar Parameters → Stock Selection → yFinance API
→ Raw Data (OHLCV) → Pandas DataFrame → Technical Analysis
→ Portfolio Logic → Tax & Profit Calculation → Visualization
→ Plotly Charts → Streamlit Dashboard → User Output

## 📊 Supported Stocks

| Symbol | Company | Sector |
|--------|---------|--------|
| HBL | Habib Bank Limited | Banking |
| UBL | United Bank Limited | Banking |
| MCB | MCB Bank Limited | Banking |
| BAFL | Bank Alfalah Limited | Banking |
| LUCK | Lucky Cement Limited | Cement |
| DGKC | Dera Ghazi Khan Cement | Cement |
| FFC | Fauji Fertilizer Company | Fertilizer |
| ENGRO | Engro Corporation | Fertilizer |
| PPL | Pakistan Petroleum Limited | Oil & Gas |
| OGDC | Oil & Gas Development Company | Oil & Gas |
| SYS | Systems Limited | Technology |
| HUBC | Hub Power Company | Power |

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| No data loading | Check internet connection. Try different stock symbol |
| yFinance timeout | Wait 30 seconds, refresh page |
| Streamlit port 8501 busy | Run `streamlit run index.py --server.port 8502` |
| Import errors | Run `pip install -r requirements.txt --upgrade` |
| Blank charts | Check browser console (F12) for errors |
| Wrong prices | PSX data may have 15-min delay on yFinance |

### Debug Mode
Add this to the top of `index.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

## 🗺️ Future Roadmap

### Version 2.0 (Planned)
- [ ] **AI Integration**: LLaMA 2 for news sentiment analysis
- [ ] **Real-time WebSocket**: Live price streaming
- [ ] **Multiple Portfolios**: Save/load different portfolios
- [ ] **Export Reports**: PDF/Excel export functionality
- [ ] **Watchlists**: Custom stock watchlists
- [ ] **Alerts**: Email/SMS price alerts

### Version 3.0 (Vision)
- [ ] **Mobile App**: React Native wrapper
- [ ] **Backtesting Engine**: Test strategies historically
- [ ] **Broker Integration**: Direct trading via PSX brokers
- [ ] **Economic Indicators**: Inflation, interest rates impact

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Areas Needing Help
- [ ] Add more PSX stocks
- [ ] Improve prediction algorithm (LSTM)
- [ ] Add more technical indicators (MACD, Stochastic)
- [ ] Create unit tests
- [ ] Translate UI to Urdu

## 📄 License

MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## 📧 Contact

**Your Name**
- LinkedIn: www.linkedin.com/in/zurriat-zehra-98b160279
- GitHub: https://github.com/zurriatzehra78-rgb/Stock-Prediction
- Email: zurriatzehra78@gmail.com

### Project Links
- Repository: `https://github.com/YOUR_USERNAME/psx-stock-predictor`
- Live Demo: https://stock-prediction-r5fwsua8s6pwfhfwwigems.streamlit.app/

## 🙏 Acknowledgments

- **yFinance** for providing free market data
- **Streamlit** for amazing UI framework
- **Pakistan Stock Exchange** for market inspiration

<div align="center">
Made with ❤️ for Pakistan Stock Exchange Investors

⭐ If you find this project useful, please give it a star on GitHub! ⭐
</div>
