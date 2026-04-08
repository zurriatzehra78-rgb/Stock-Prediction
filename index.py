import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="PSX Stock Predictor - Real-Time",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Set main background to black */
    .stApp {
        background-color: black;
    }
    
    /* Update text colors for better contrast on black background */
    .stMarkdown, .stText, .stNumberInput, .stSelectbox, .stMultiSelect {
        color: white;
    }
    
    /* Keep all original styles */
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .success-box {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

class StockPredictorUI:
    def __init__(self):
        # Define PSX stocks with their Yahoo Finance symbols
        self.psx_stocks = {
            'ENGRO': {
                'symbol': 'ENGRO.PSX',
                'name': 'ENGRO Corporation Limited',
                'sector': 'Fertilizer'
            },
            'HBL': {
                'symbol': 'HBL.PSX',
                'name': 'Habib Bank Limited',
                'sector': 'Banking'
            },
            'LUCKY': {
                'symbol': 'LUCKY.PSX',
                'name': 'Lucky Cement Limited',
                'sector': 'Cement'
            },
            'OGDC': {
                'symbol': 'OGDC.PSX',
                'name': 'Oil & Gas Development Company',
                'sector': 'Oil & Gas'
            },
            'PPL': {
                'symbol': 'PPL.PSX',
                'name': 'Pakistan Petroleum Limited',
                'sector': 'Oil & Gas'
            },
            'UBL': {
                'symbol': 'UBL.PSX',
                'name': 'United Bank Limited',
                'sector': 'Banking'
            },
            'MCB': {
                'symbol': 'MCB.PSX',
                'name': 'MCB Bank Limited',
                'sector': 'Banking'
            },
            'POL': {
                'symbol': 'POL.PSX',
                'name': 'Pakistan Oilfields Limited',
                'sector': 'Oil & Gas'
            },
            'FFC': {
                'symbol': 'FFC.PSX',
                'name': 'Fauji Fertilizer Company',
                'sector': 'Fertilizer'
            },
            'NESTLE': {
                'symbol': 'NESTLE.PSX',
                'name': 'Nestle Pakistan Limited',
                'sector': 'Food'
            },
            'SYS': {
                'symbol': 'SYS.PSX',
                'name': 'Systems Limited',
                'sector': 'Technology'
            },
            'TRG': {
                'symbol': 'TRG.PSX',
                'name': 'TRG Pakistan Limited',
                'sector': 'Technology'
            }
        }
        self.current_stock = None
        self.data = None
        self.stock_info = None

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_stock_data(_self, symbol, period='6mo'):
        """Fetch real-time stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Fetch historical data
            hist = ticker.history(period=period, interval='1d')
            
            if hist.empty:
                return None
            
            # Get current price and other metrics
            current_price = hist['Close'].iloc[-1]
            
            # Get company info
            info = ticker.info
            
            # Calculate returns and volatility
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            # Prepare data
            data = {
                'dates': hist.index.strftime('%b %Y').tolist(),
                'prices': hist['Close'].round(2).tolist(),
                'volumes': hist['Volume'].tolist(),
                'high': hist['High'].tolist(),
                'low': hist['Low'].tolist(),
                'open': hist['Open'].tolist(),
                'returns': returns.tolist(),
                'current_price': current_price,
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A',
                'dividend_yield': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
                'volume_avg': hist['Volume'].mean(),
                'volatility': round(volatility * 100, 2),
                '52_week_high': info.get('fiftyTwoWeekHigh', current_price),
                '52_week_low': info.get('fiftyTwoWeekLow', current_price),
                'beta': round(info.get('beta', 1), 2) if info.get('beta') else 1
            }
            
            return data
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def calculate_moving_average(self, prices, window=3):
        """Calculate simple moving average"""
        ma = []
        for i in range(len(prices)):
            if i < window - 1:
                ma.append(None)
            else:
                avg = sum(prices[i-window+1:i+1]) / window
                ma.append(round(avg, 2))
        return ma

    def calculate_technical_indicators(self, prices):
        """Calculate various technical indicators"""
        # RSI (Relative Strength Index)
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(change if change > 0 else 0)
            losses.append(abs(change) if change < 0 else 0)
        
        # Use at least 14 periods or available data
        periods = min(14, len(gains))
        avg_gain = sum(gains[-periods:]) / periods if periods > 0 else 0
        avg_loss = sum(losses[-periods:]) / periods if periods > 0 else 1
        
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 50
        
        # MACD (Moving Average Convergence Divergence)
        ema12 = self.calculate_ema(prices, min(12, len(prices)))
        ema26 = self.calculate_ema(prices, min(26, len(prices)))
        macd_line = ema12[-1] - ema26[-1] if ema12 and ema26 else 0
        
        # Bollinger Bands
        window = min(20, len(prices))
        sma20 = sum(prices[-window:]) / window
        std20 = np.std(prices[-window:]) if len(prices) >= window else np.std(prices)
        upper_band = sma20 + (std20 * 2)
        lower_band = sma20 - (std20 * 2)
        
        # Moving averages
        ma20 = sum(prices[-min(20, len(prices)):]) / min(20, len(prices))
        ma50 = sum(prices[-min(50, len(prices)):]) / min(50, len(prices))
        
        return {
            'RSI': round(rsi, 2),
            'MACD': round(macd_line, 2),
            'Upper Band': round(upper_band, 2),
            'Lower Band': round(lower_band, 2),
            'MA20': round(ma20, 2),
            'MA50': round(ma50, 2)
        }

    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            period = len(prices)
        if period <= 0:
            return [prices[-1]]
        
        multiplier = 2 / (period + 1)
        ema = [prices[0]]
        for price in prices[1:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        return ema

    def calculate_trend(self, prices):
        """Calculate trend percentage"""
        if len(prices) < 2:
            return 0
        change = ((prices[-1] - prices[0]) / prices[0]) * 100
        return change

    def predict_future(self, months=5):
        """Simple prediction based on linear trend with exponential smoothing"""
        prices = self.data['prices']
        
        n = len(prices)
        x = list(range(n))
        y = prices
        
        # Simple linear regression with more weight to recent data
        weights = [1 + 0.2 * (i/n) for i in range(n)]  # Weight recent data more
        weighted_sum = sum(weights)
        
        mean_x = sum(x[i] * weights[i] for i in range(n)) / weighted_sum
        mean_y = sum(y[i] * weights[i] for i in range(n)) / weighted_sum
        
        numerator = sum(weights[i] * (x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum(weights[i] * ((x[i] - mean_x) ** 2) for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = mean_y - slope * mean_x
        
        # Predict future prices with momentum factor
        momentum = (y[-1] - y[-min(5, len(y))]) / y[-min(5, len(y))] if len(y) >= 5 else 0
        
        predictions = []
        for i in range(n, n + months):
            pred_price = slope * i + intercept
            # Add momentum for more realistic predictions
            pred_price = pred_price * (1 + momentum * 0.3)
            predictions.append(round(pred_price, 2))
        
        # Calculate confidence intervals (95%)
        residuals = [y[i] - (slope * x[i] + intercept) for i in range(n)]
        std_dev = math.sqrt(sum(r**2 for r in residuals) / n) if n > 0 else 0
        
        lower_bounds = [round(p - 1.96 * std_dev, 2) for p in predictions]
        upper_bounds = [round(p + 1.96 * std_dev, 2) for p in predictions]
        
        return predictions, lower_bounds, upper_bounds

    def create_interactive_chart(self):
        """Create interactive Plotly chart with historical and predicted data"""
        historical_prices = self.data['prices']
        historical_dates = pd.date_range(
            start=datetime.now() - timedelta(days=len(historical_prices)),
            periods=len(historical_prices),
            freq='D'
        )
        
        predicted_prices, lower_bounds, upper_bounds = self.predict_future()
        future_dates = pd.date_range(
            start=historical_dates[-1] + timedelta(days=1),
            periods=len(predicted_prices),
            freq='MS'
        )
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Price Chart with Technical Indicators', 'Trading Volume', 'RSI Indicator'),
            vertical_spacing=0.08,
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Candlestick chart for historical data
        fig.add_trace(
            go.Candlestick(
                x=historical_dates,
                open=self.data['open'],
                high=self.data['high'],
                low=self.data['low'],
                close=historical_prices,
                name='Historical',
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Add moving averages
        ma20 = self.calculate_moving_average(historical_prices, 20)
        ma50 = self.calculate_moving_average(historical_prices, 50)
        
        fig.add_trace(
            go.Scatter(
                x=historical_dates,
                y=ma20,
                mode='lines',
                name='MA 20',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=historical_dates,
                y=ma50,
                mode='lines',
                name='MA 50',
                line=dict(color='red', width=1)
            ),
            row=1, col=1
        )
        
        # Predicted data with confidence intervals
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=predicted_prices,
                mode='lines+markers',
                name='Predicted',
                line=dict(color='orange', dash='dash', width=2),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Confidence intervals
        fig.add_trace(
            go.Scatter(
                x=future_dates.tolist() + future_dates.tolist()[::-1],
                y=upper_bounds + lower_bounds[::-1],
                fill='toself',
                fillcolor='rgba(255, 165, 0, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence Interval',
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Volume bars with color coding
        colors = ['green' if self.data['prices'][i] >= self.data['open'][i] else 'red' 
                  for i in range(len(self.data['volumes']))]
        fig.add_trace(
            go.Bar(
                x=historical_dates,
                y=self.data['volumes'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # RSI Indicator
        tech_indicators = self.calculate_technical_indicators(historical_prices)
        rsi_values = []
        for i in range(len(historical_prices)):
            if i < 14:
                rsi_values.append(None)
            else:
                rsi_values.append(tech_indicators['RSI'])
        
        fig.add_trace(
            go.Scatter(
                x=historical_dates,
                y=rsi_values,
                mode='lines',
                name='RSI (14)',
                line=dict(color='purple', width=2)
            ),
            row=3, col=1
        )
        
        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        # Update layout
        fig.update_layout(
            title=f'{self.current_stock} - Real-Time Stock Analysis & Prediction',
            yaxis_title='Price (PKR)',
            xaxis_title='Date',
            template='plotly_dark',
            height=800,
            hovermode='x unified',
            showlegend=True
        )
        
        fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
        fig.update_yaxes(title_text="Price (PKR)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])
        
        return fig

    def analyze_investment(self, invested_amount, target_profit, tax_rate, utilities_rate):
        """Analyze investment based on predictions"""
        current_price = self.data['current_price']
        historical_prices = self.data['prices']
        shares = invested_amount / current_price
        
        # Get predictions
        predicted_prices, lower_bounds, upper_bounds = self.predict_future()
        
        # Calculate target requirements
        target_net_profit = invested_amount * (target_profit / 100)
        tax_amount = target_net_profit * (tax_rate / 100)
        utilities = target_net_profit * (utilities_rate / 100)
        required_gross_profit = target_net_profit + tax_amount + utilities
        required_price = current_price + (required_gross_profit / shares)
        
        # Calculate trends
        historical_change = ((historical_prices[-1] - historical_prices[0]) / historical_prices[0]) * 100
        predicted_high = max(predicted_prices)
        predicted_low = min(predicted_prices)
        predicted_change = ((predicted_prices[-1] - current_price) / current_price) * 100
        expected_return = ((predicted_prices[-1] - current_price) / current_price) * 100
        
        # Calculate risk metrics
        tech_indicators = self.calculate_technical_indicators(historical_prices)
        rsi = tech_indicators['RSI']
        
        # Enhanced decision logic with technical analysis
        score = 0
        
        # Trend score
        if predicted_change > 10:
            score += 3
        elif predicted_change > 5:
            score += 2
        elif predicted_change > 0:
            score += 1
        
        # RSI score
        if 30 <= rsi <= 70:
            score += 2
        elif rsi < 30:  # Oversold - good buying opportunity
            score += 3
        elif rsi > 70:  # Overbought - caution
            score -= 1
        
        # Target achievability
        if predicted_high >= required_price:
            score += 2
        
        # Make decision based on score
        if score >= 6:
            decision = "STRONG BUY"
            color = "success"
            reason = f"Excellent opportunity! Score: {score}/8. Strong upward momentum with favorable technical indicators."
        elif score >= 4:
            decision = "BUY"
            color = "success"
            reason = f"Good potential with score: {score}/8. Positive outlook with {predicted_change:.1f}% predicted growth."
        elif score >= 2:
            decision = "HOLD"
            color = "info"
            reason = f"Moderate potential (Score: {score}/8). Monitor closely before adding more position."
        elif score >= 0:
            decision = "MONITOR"
            color = "warning"
            reason = f"Uncertain outlook (Score: {score}/8). Consider partial position or wait for better entry."
        else:
            decision = "SELL"
            color = "danger"
            reason = f"Negative outlook (Score: {score}/8) with {predicted_change:.1f}% predicted drop. Exit or reduce position recommended."
        
        return {
            'decision': decision,
            'color': color,
            'reason': reason,
            'current_price': current_price,
            'shares': shares,
            'historical_change': historical_change,
            'predicted_change': predicted_change,
            'predicted_high': predicted_high,
            'predicted_low': predicted_low,
            'required_price': required_price,
            'expected_return': expected_return,
            'predicted_prices': predicted_prices,
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'score': score,
            'rsi': rsi
        }

def main():
    st.title("📈 Pakistan Stock Exchange (PSX) Real-Time Stock Predictor")
    st.markdown("*Powered by Yahoo Finance Real-Time Data*")
    st.markdown("---")
    
    # Initialize predictor
    if 'predictor' not in st.session_state:
        st.session_state.predictor = StockPredictorUI()
    
    predictor = st.session_state.predictor
    
    # Sidebar for stock selection
    with st.sidebar:
        st.header("📊 Stock Selection")
        
        # Add search/filter
        sector_filter = st.selectbox(
            "Filter by sector:",
            ["All"] + list(set(predictor.psx_stocks[s]['sector'] for s in predictor.psx_stocks))
        )
        
        # Filter stocks
        filtered_stocks = predictor.psx_stocks
        if sector_filter != "All":
            filtered_stocks = {k: v for k, v in predictor.psx_stocks.items() if v['sector'] == sector_filter}
        
        stock_symbol = st.selectbox(
            "Choose a stock to analyze:",
            options=list(filtered_stocks.keys()),
            format_func=lambda x: f"{x} - {filtered_stocks[x]['name']}"
        )
        
        # Data period selection
        period = st.selectbox(
            "Historical data period:",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=2
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Analyze Stock", use_container_width=True):
                with st.spinner(f"Fetching real-time data for {stock_symbol}..."):
                    predictor.current_stock = stock_symbol
                    predictor.data = predictor.fetch_stock_data(
                        predictor.psx_stocks[stock_symbol]['symbol'], 
                        period
                    )
                    if predictor.data:
                        st.session_state.analyzed = True
                        st.rerun()
                    else:
                        st.error("Failed to fetch data. Please try again.")
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                if hasattr(st.session_state, 'analyzed') and st.session_state.analyzed:
                    with st.spinner("Refreshing data..."):
                        predictor.data = predictor.fetch_stock_data(
                            predictor.psx_stocks[predictor.current_stock]['symbol'],
                            period
                        )
                        st.rerun()
        
        st.markdown("---")
        
        # Market summary
        st.header("📊 Market Summary")
        
        # Calculate market indicators
        if hasattr(st.session_state, 'analyzed') and st.session_state.analyzed and predictor.data:
            tech_indicators = predictor.calculate_technical_indicators(predictor.data['prices'])
            
            st.metric("Market Sentiment", 
                     "Bullish" if tech_indicators['RSI'] < 70 else "Bearish",
                     delta=f"RSI: {tech_indicators['RSI']}")
            
            st.metric("Volatility Index", 
                     f"{predictor.data['volatility']}%",
                     delta="High Risk" if predictor.data['volatility'] > 30 else "Moderate Risk")
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info(
            "**Real-Time PSX Stock Predictor**\n\n"
            "• Fetches live data from Yahoo Finance\n"
            "• Uses Linear Regression with momentum factor\n"
            "• Includes technical indicators (RSI, MACD, Bollinger Bands)\n"
            "• Provides Buy/Hold/Sell recommendations\n\n"
            "*Note: This is for educational purposes. Consult a financial advisor before investing.*"
        )
    
    # Main content area
    if hasattr(st.session_state, 'analyzed') and st.session_state.analyzed and predictor.data:
        stock_info = predictor.psx_stocks[predictor.current_stock]
        
        # Last updated timestamp
        st.caption(f"📡 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Stock header with metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Current Price", f"PKR {predictor.data['current_price']:.2f", 
                     delta=f"{predictor.calculate_trend(predictor.data['prices']):.1f}%")
        with col2:
            st.metric("Market Cap", predictor.data['market_cap'] if isinstance(predictor.data['market_cap'], str) 
                     else f"PKR {predictor.data['market_cap']/1e9:.1f}B")
        with col3:
            st.metric("P/E Ratio", predictor.data['pe_ratio'])
        with col4:
            st.metric("Dividend Yield", f"{predictor.data['dividend_yield']}%")
        with col5:
            st.metric("Beta", predictor.data['beta'])
        
        st.markdown("---")
        
        # Additional metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("52-Week High", f"PKR {predictor.data['52_week_high']:.2f}")
        with col2:
            st.metric("52-Week Low", f"PKR {predictor.data['52_week_low']:.2f}")
        with col3:
            st.metric("Avg Volume", f"{int(predictor.data['volume_avg']):,}")
        with col4:
            st.metric("Volatility (Annual)", f"{predictor.data['volatility']}%")
        
        st.markdown("---")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Interactive Chart", "📊 Technical Analysis", "💼 Investment Analysis", "📅 Predictions", "📰 Stock Info"])
        
        with tab1:
            st.subheader(f"{predictor.current_stock} - Real-Time Price Chart with Predictions")
            fig = predictor.create_interactive_chart()
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Technical Analysis Dashboard")
            
            # Calculate technical indicators
            tech_indicators = predictor.calculate_technical_indicators(predictor.data['prices'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("### 📊 Momentum Indicators")
                st.metric("RSI (14)", tech_indicators['RSI'], 
                         delta="Overbought" if tech_indicators['RSI'] > 70 else ("Oversold" if tech_indicators['RSI'] < 30 else "Neutral"))
                st.metric("MACD", tech_indicators['MACD'])
                st.metric("Beta", predictor.data['beta'])
                
            with col2:
                st.markdown("### 📉 Volatility Indicators")
                st.metric("Bollinger Upper", f"PKR {tech_indicators['Upper Band']:.2f}")
                st.metric("Bollinger Lower", f"PKR {tech_indicators['Lower Band']:.2f}")
                current_price = predictor.data['current_price']
                band_position = ((current_price - tech_indicators['Lower Band']) / 
                               (tech_indicators['Upper Band'] - tech_indicators['Lower Band'])) * 100 if tech_indicators['Upper Band'] != tech_indicators['Lower Band'] else 50
                st.progress(int(band_position))
                st.caption(f"Price position within bands: {band_position:.1f}%")
            
            with col3:
                st.markdown("### 📈 Trend Indicators")
                st.metric("MA (20)", f"PKR {tech_indicators['MA20']:.2f}")
                st.metric("MA (50)", f"PKR {tech_indicators['MA50']:.2f}")
                trend = "Bullish" if tech_indicators['MA20'] > tech_indicators['MA50'] else "Bearish"
                st.metric("Trend", trend)
            
            st.markdown("---")
            
            # Historical data table
            st.subheader("Historical Data")
            hist_df = pd.DataFrame({
                'Date': predictor.data['dates'],
                'Open': predictor.data['open'],
                'High': predictor.data['high'],
                'Low': predictor.data['low'],
                'Close': predictor.data['prices'],
                'Volume': predictor.data['volumes'],
                'Returns %': [round(r*100, 2) if r else 0 for r in predictor.data['returns']]
            })
            st.dataframe(hist_df.tail(20), use_container_width=True)
        
        with tab3:
            st.subheader("Investment Analysis & Recommendations")
            
            # Input form for investment parameters
            with st.form("investment_form"):
                col1, col2 = st.columns(2)
                with col1:
                    invested_amount = st.number_input("💰 Investment Amount (PKR)", 
                                                     min_value=1000.0, 
                                                     value=100000.0, 
                                                     step=10000.0,
                                                     format="%.2f")
                    target_profit = st.number_input("🎯 Target Profit (%)", 
                                                    min_value=1.0, 
                                                    max_value=100.0, 
                                                    value=10.0, 
                                                    step=1.0)
                
                with col2:
                    use_custom = st.checkbox("Use custom tax & utilities rates")
                    if use_custom:
                        tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=50.0, value=15.0)
                        utilities_rate = st.number_input("Utilities Fee Rate (%)", min_value=0.0, max_value=20.0, value=5.0)
                    else:
                        tax_rate = 15.0
                        utilities_rate = 5.0
                        st.info("Default rates: Capital Gains Tax = 15%, Brokerage + Fees = 5%")
                
                submitted = st.form_submit_button("🔍 Analyze Investment", use_container_width=True)
            
            if submitted:
                with st.spinner("Analyzing investment opportunity..."):
                    analysis = predictor.analyze_investment(invested_amount, target_profit, tax_rate, utilities_rate)
                    
                    # Display decision with appropriate styling
                    if analysis['color'] == 'success':
                        st.success(f"### 🎯 DECISION: {analysis['decision']} (Score: {analysis['score']}/8)")
                        st.success(f"**Reason:** {analysis['reason']}")
                    elif analysis['color'] == 'warning':
                        st.warning(f"### ⚠️ DECISION: {analysis['decision']} (Score: {analysis['score']}/8)")
                        st.warning(f"**Reason:** {analysis['reason']}")
                    elif analysis['color'] == 'danger':
                        st.error(f"### ❌ DECISION: {analysis['decision']} (Score: {analysis['score']}/8)")
                        st.error(f"**Reason:** {analysis['reason']}")
                    else:
                        st.info(f"### ℹ️ DECISION: {analysis['decision']} (Score: {analysis['score']}/8)")
                        st.info(f"**Reason:** {analysis['reason']}")
                    
                    # Detailed analysis
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current Price", f"PKR {analysis['current_price']:.2f}")
                        st.metric("Shares You Can Buy", f"{analysis['shares']:.0f}")
                    
                    with col2:
                        st.metric("Required Price for Target", f"PKR {analysis['required_price']:.2f}")
                        price_gap = analysis['required_price'] - analysis['current_price']
                        st.metric("Price Gap", f"PKR {price_gap:.2f}", 
                                 delta="Achievable" if price_gap <= (analysis['predicted_high'] - analysis['current_price']) else "Challenging")
                    
                    with col3:
                        st.metric("Expected Return (5 months)", f"{analysis['expected_return']:+.1f}%")
                        st.metric("Predicted Range", f"PKR {analysis['predicted_low']:.2f} - {analysis['predicted_high']:.2f}")
                    
                    # Risk assessment
                    st.markdown("---")
                    st.subheader("📊 Risk Assessment")
                    
                    risk_col1, risk_col2, risk_col3 = st.columns(3)
                    with risk_col1:
                        st.metric("Current RSI", analysis['rsi'])
                        if analysis['rsi'] > 70:
                            st.warning("⚠️ Stock is overbought - potential pullback risk")
                        elif analysis['rsi'] < 30:
                            st.success("✅ Stock is oversold - potential buying opportunity")
                        else:
                            st.info("ℹ️ RSI is in neutral zone")
                    
                    with risk_col2:
                        st.metric("Volatility Risk", f"{predictor.data['volatility']}%")
                        if predictor.data['volatility'] > 40:
                            st.warning("⚠️ High volatility stock - use strict stop-loss")
                        elif predictor.data['volatility'] > 25:
                            st.info("📊 Moderate volatility - standard risk management")
                        else:
                            st.success("✅ Low volatility - relatively stable")
                    
                    with risk_col3:
                        st.metric("Beta (Market Risk)", predictor.data['beta'])
                        if predictor.data['beta'] > 1.2:
                            st.warning("⚠️ Stock moves more than market - higher risk")
                        elif predictor.data['beta'] < 0.8:
                            st.info("📊 Defensive stock - lower market correlation")
                        else:
                            st.success("✅ Beta near market average")
                    
                    # Recommendations
                    st.markdown("---")
                    st.subheader("📋 Actionable Recommendations")
                    
                    if "BUY" in analysis['decision']:
                        st.markdown(f"""
                        ### ✅ Recommended Action Plan:
                        
                        1. **Entry Strategy:**
                           - 🟢 **Aggressive Entry:** Buy at current price (PKR {analysis['current_price']:.2f})
                           - 🟡 **Conservative Entry:** Place limit order at PKR {analysis['current_price'] * 0.97:.2f} (3% below current)
                           - 📊 **Dollar Cost Average:** Split investment into 3 parts over 2-3 weeks
                        
                        2. **Exit Strategy:**
                           - 🎯 **Target 1 (50% profit):** PKR {(analysis['current_price'] + (analysis['predicted_high'] - analysis['current_price'])/2):.2f}
                           - 🎯 **Target 2 (Full profit):** PKR {analysis['predicted_high']:.2f}
                        """)
                    elif "HOLD" in analysis['decision']:
                        st.markdown("""
                        ### 📊 Hold Strategy:
                        
                        1. **Current Position:**
                           - Maintain current holdings
                           - Set stop-loss at 5-7% below current price
                           - Wait for clearer signals
                        
                        2. **Watch Points:**
                           - Monitor RSI for entry opportunities
                           - Watch for breakout above resistance
                           - Consider partial profit booking if price spikes
                        """)
                    elif "SELL" in analysis['decision']:
                        st.markdown("""
                        ### 🔴 Exit Strategy:
                        
                        1. **Immediate Actions:**
                           - Consider selling 50-70% of position
                           - Set tight stop-loss at 3-5%
                           - Reduce exposure to this stock
                        
                        2. **Alternative Actions:**
                           - Shift capital to better opportunities
                           - Wait for pullback to exit remaining position
                           - Consider hedging strategies
                        """)
                    else:
                        st.markdown("""
                        ### 📈 Monitoring Strategy:
                        
                        1. **Wait and Watch:**
                           - Hold cash position for now
                           - Set price alerts at key levels
                           - Monitor technical indicators daily
                        
                        2. **Entry Conditions:**
                           - Wait for RSI to reach oversold levels (<30)
                           - Look for bullish reversal patterns
                           - Enter only if price breaks resistance with volume
                        """)
        
        with tab4:
            st.subheader("Future Price Predictions")
            predicted_prices, lower_bounds, upper_bounds = predictor.predict_future()
            
            # Create prediction table
            months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5"]
            pred_df = pd.DataFrame({
                'Month': months,
                'Predicted Price (PKR)': predicted_prices,
                'Lower Bound (95% CI)': lower_bounds,
                'Upper Bound (95% CI)': upper_bounds
            })
            st.dataframe(pred_df, use_container_width=True)
            
            # Prediction chart
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=months,
                y=predicted_prices,
                mode='lines+markers',
                name='Predicted Price',
                line=dict(color='orange', width=2),
                marker=dict(size=10)
            ))
            fig_pred.add_trace(go.Scatter(
                x=months,
                y=upper_bounds,
                mode='lines',
                name='Upper Bound (95% CI)',
                line=dict(color='gray', dash='dash')
            ))
            fig_pred.add_trace(go.Scatter(
                x=months,
                y=lower_bounds,
                mode='lines',
                name='Lower Bound (95% CI)',
                line=dict(color='gray', dash='dash')
            ))
            fig_pred.update_layout(
                title='5-Month Price Prediction',
                xaxis_title='Time Period',
                yaxis_title='Price (PKR)',
                template='plotly_dark',
                height=500
            )
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Prediction insights
            st.subheader("📊 Prediction Insights")
            col1, col2, col3 = st.columns(3)
            with col1:
                expected_return = ((predicted_prices[-1] - predictor.data['current_price']) / predictor.data['current_price']) * 100
                st.metric("Expected Return (5 months)", f"{expected_return:+.1f}%")
            with col2:
                st.metric("Maximum Price", f"PKR {max(predicted_prices):.2f}")
            with col3:
                st.metric("Minimum Price", f"PKR {min(predicted_prices):.2f}")
        
        with tab5:
            st.subheader("Company Information")
            st.markdown(f"""
            ### {stock_info['name']} ({predictor.current_stock})
            
            **Sector:** {stock_info['sector']}
            
            **About:**
            {predictor.current_stock} is a leading company in Pakistan's {stock_info['sector']} sector.
            
            **Key Metrics:**
            - Current Price: PKR {predictor.data['current_price']:.2f}
            - Market Cap: {predictor.data['market_cap'] if isinstance(predictor.data['market_cap'], str) else f'PKR {predictor.data["market_cap"]/1e9:.1f}B'}
            - P/E Ratio: {predictor.data['pe_ratio']}
            - Dividend Yield: {predictor.data['dividend_yield']}%
            - Beta: {predictor.data['beta']}
            - 52-Week Range: PKR {predictor.data['52_week_low']:.2f} - {predictor.data['52_week_high']:.2f}
            
            **Volatility Information:**
            - Annual Volatility: {predictor.data['volatility']}%
            - Average Daily Volume: {int(predictor.data['volume_avg']):,}
            
            *Data provided by Yahoo Finance*
            """)

if __name__ == "__main__":
    main()