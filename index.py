import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="PSX Stock Predictor - Professional Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Make ALL main page text white */
    .stMarkdown, .stText, .stNumberInput, .stSelectbox, .stMultiSelect, label, .stMetric label, .stMetric p {
        color: white !important;
    }
    
    /* Make metric values white */
    .stMetric .css-1xarl3l, .stMetric .css-1wivap2, .stMetric div {
        color: white !important;
    }
    
    /* Make dataframe text white */
    .dataframe, .dataframe td, .dataframe th {
        color: white !important;
        background-color: rgba(0,0,0,0.5) !important;
    }
    
    /* SIDEBAR - Make text BLACK */
    .css-1d391kg, .css-1d391kg .stMarkdown, .css-1d391kg label, .css-1d391kg p, 
    .css-1d391kg .stText, .css-1d391kg .stNumberInput, .css-1d391kg .stSelectbox,
    .css-1d391kg .stMultiSelect, .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    .css-1d391kg .stAlert, .css-1d391kg .stInfo, .css-1d391kg .stWarning {
        color: #1a1a1a !important;
    }
    
    /* Sidebar header text */
    .css-1d391kg .stHeader, .css-1d391kg header {
        color: #1a1a1a !important;
    }
    
    /* Sidebar metric text */
    .css-1d391kg .stMetric label, .css-1d391kg .stMetric p {
        color: #1a1a1a !important;
    }
    
    /* Sidebar number input values */
    .css-1d391kg .stNumberInput input, .css-1d391kg .stTextInput input {
        color: #1a1a1a !important;
        background-color: white !important;
    }
    
    /* Sidebar select box */
    .css-1d391kg .stSelectbox div, .css-1d391kg .stSelectbox label {
        color: #1a1a1a !important;
    }
    
    /* Keep PSX Stock Predictor title with gradient */
    h1 {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
    }
    
    /* Tab text */
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }
    
    /* Main content input text */
    .stTextInput input, .stNumberInput input {
        color: white !important;
        background-color: rgba(0,0,0,0.5) !important;
    }
    
    /* Caption text */
    .stCaption, caption {
        color: rgba(255,255,255,0.7) !important;
    }
    
    /* Sidebar divider lines */
    hr {
        border-color: rgba(0,0,0,0.2) !important;
    }
    
    /* CHANGE: Instruction text in BLACK (was red) */
    .instruction-text {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        margin-bottom: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

class PSXStockPredictor:
    def __init__(self):
        # PSX Stocks with verified working symbols
        self.psx_stocks = {
            'HBL': {'symbol': 'HBL', 'name': 'Habib Bank Limited', 'sector': 'Banking', 'currency': 'PKR'},
            'UBL': {'symbol': 'UBL', 'name': 'United Bank Limited', 'sector': 'Banking', 'currency': 'PKR'},
            'MCB': {'symbol': 'MCB', 'name': 'MCB Bank Limited', 'sector': 'Banking', 'currency': 'PKR'},
            'BAFL': {'symbol': 'BAFL', 'name': 'Bank Alfalah Limited', 'sector': 'Banking', 'currency': 'PKR'},
            'LUCK': {'symbol': 'LUCK', 'name': 'Lucky Cement Limited', 'sector': 'Cement', 'currency': 'PKR'},
            'DGKC': {'symbol': 'DGKC', 'name': 'Dera Ghazi Khan Cement', 'sector': 'Cement', 'currency': 'PKR'},
            'FFC': {'symbol': 'FFC', 'name': 'Fauji Fertilizer Company', 'sector': 'Fertilizer', 'currency': 'PKR'},
            'ENGRO': {'symbol': 'ENGRO', 'name': 'Engro Corporation', 'sector': 'Fertilizer', 'currency': 'PKR'},
            'PPL': {'symbol': 'PPL', 'name': 'Pakistan Petroleum Limited', 'sector': 'Oil & Gas', 'currency': 'PKR'},
            'OGDC': {'symbol': 'OGDC', 'name': 'Oil & Gas Development Company', 'sector': 'Oil & Gas', 'currency': 'PKR'},
            'SYS': {'symbol': 'SYS', 'name': 'Systems Limited', 'sector': 'Technology', 'currency': 'PKR'},
            'HUBC': {'symbol': 'HUBC', 'name': 'Hub Power Company', 'sector': 'Power', 'currency': 'PKR'},
        }
        
        self.current_stock = None
        self.data = None
        self.purchase_price_per_share = None
        self.total_purchase_price = None
        self.required_profit_percent = None
        self.tax_rate = None
        self.utilities_rate = None

    @st.cache_data(ttl=300)
    def fetch_stock_data(_self, symbol, period='6mo'):
        symbols_to_try = [f"{symbol}.PK", f"{symbol}.PSX", symbol, f"{symbol}.KA", f"{symbol}-PK"]
        
        for try_symbol in symbols_to_try:
            try:
                ticker = yf.Ticker(try_symbol)
                hist = ticker.history(period=period, interval='1d')
                
                if not hist.empty and len(hist) > 5:
                    current_price = hist['Close'].iloc[-1]
                    info = ticker.info
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252)
                    
                    data = {
                        'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                        'prices': hist['Close'].round(2).tolist(),
                        'volumes': hist['Volume'].tolist(),
                        'high': hist['High'].round(2).tolist(),
                        'low': hist['Low'].round(2).tolist(),
                        'open': hist['Open'].round(2).tolist(),
                        'current_price': current_price,
                        'market_cap': info.get('marketCap', 'N/A'),
                        'pe_ratio': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A',
                        'dividend_yield': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
                        'volume_avg': hist['Volume'].mean(),
                        'volatility': round(volatility * 100, 2),
                        '52_week_high': info.get('fiftyTwoWeekHigh', current_price),
                        '52_week_low': info.get('fiftyTwoWeekLow', current_price),
                        'beta': round(info.get('beta', 1), 2) if info.get('beta') else 1,
                    }
                    return data
            except Exception:
                continue
        
        st.warning(f"Using simulated data for {symbol}")
        return _self.generate_sample_data(symbol, period)
    
    def generate_sample_data(self, symbol, period='6mo'):
        days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}[period]
        base_price = 100 + np.random.randint(50, 500)
        dates = [(datetime.now() - timedelta(days=x)) for x in range(days, 0, -1)]
        returns = np.random.normal(0.001, 0.02, days)
        prices = [base_price]
        for ret in returns:
            prices.append(prices[-1] * (1 + ret))
        prices = prices[1:]
        
        data = {
            'dates': [d.strftime('%Y-%m-%d') for d in dates],
            'prices': [round(p, 2) for p in prices],
            'volumes': [int(np.random.uniform(100000, 1000000)) for _ in range(days)],
            'high': [round(p * (1 + np.random.uniform(0, 0.02)), 2) for p in prices],
            'low': [round(p * (1 - np.random.uniform(0, 0.02)), 2) for p in prices],
            'open': [round(p * (1 + np.random.uniform(-0.01, 0.01)), 2) for p in prices],
            'current_price': round(prices[-1], 2),
            'market_cap': f"PKR {np.random.uniform(10, 500):.1f}B",
            'pe_ratio': round(np.random.uniform(5, 25), 2),
            'dividend_yield': round(np.random.uniform(2, 12), 2),
            'volume_avg': int(np.random.uniform(500000, 2000000)),
            'volatility': round(np.random.uniform(15, 45), 2),
            '52_week_high': round(max(prices) * 1.05, 2),
            '52_week_low': round(min(prices) * 0.95, 2),
            'beta': round(np.random.uniform(0.5, 1.5), 2),
        }
        return data

    def calculate_technical_indicators(self, prices):
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(change if change > 0 else 0)
            losses.append(abs(change) if change < 0 else 0)
        
        periods = min(14, len(gains))
        avg_gain = sum(gains[-periods:]) / periods if periods > 0 else 0
        avg_loss = sum(losses[-periods:]) / periods if periods > 0 else 1
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        
        ma20 = sum(prices[-min(20, len(prices)):]) / min(20, len(prices))
        ma50 = sum(prices[-min(50, len(prices)):]) / min(50, len(prices))
        
        window = min(20, len(prices))
        sma20 = sum(prices[-window:]) / window
        std20 = np.std(prices[-window:]) if len(prices) >= window else np.std(prices)
        upper_band = sma20 + (std20 * 2)
        lower_band = sma20 - (std20 * 2)
        
        return {
            'RSI': round(rsi, 2),
            'MA20': round(ma20, 2),
            'MA50': round(ma50, 2),
            'Upper Band': round(upper_band, 2),
            'Lower Band': round(lower_band, 2),
        }

    def calculate_trend(self, prices):
        if len(prices) < 2:
            return 0
        return ((prices[-1] - prices[0]) / prices[0]) * 100

    def predict_future(self, months=5):
        prices = self.data['prices']
        n = len(prices)
        x = list(range(n))
        y = prices
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = mean_y - slope * mean_x
        
        predictions = [round(slope * i + intercept, 2) for i in range(n, n + months)]
        
        residuals = [y[i] - (slope * x[i] + intercept) for i in range(n)]
        std_dev = math.sqrt(sum(r**2 for r in residuals) / n) if n > 0 else 0
        
        lower_bounds = [round(p - 1.96 * std_dev, 2) for p in predictions]
        upper_bounds = [round(p + 1.96 * std_dev, 2) for p in predictions]
        
        return predictions, lower_bounds, upper_bounds

def main():
    st.markdown("<h1>PSX Stock Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Real-Time Pakistan Stock Exchange Analysis</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize
    if 'predictor' not in st.session_state:
        st.session_state.predictor = PSXStockPredictor()
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
    
    predictor = st.session_state.predictor
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Stock Selection")
        
        sectors = ["All"] + sorted(list(set(predictor.psx_stocks[s]['sector'] for s in predictor.psx_stocks)))
        sector_filter = st.selectbox("Filter by Sector", sectors)
        
        filtered_stocks = predictor.psx_stocks
        if sector_filter != "All":
            filtered_stocks = {k: v for k, v in predictor.psx_stocks.items() if v['sector'] == sector_filter}
        
        stock_symbol = st.selectbox(
            "Select Stock",
            options=list(filtered_stocks.keys()),
            format_func=lambda x: f"{x} - {filtered_stocks[x]['name']}"
        )
        
        period = st.selectbox("Data Period", ["1mo", "3mo", "6mo", "1y"], index=2)
        
        # Investment Parameters
        st.markdown("---")
        st.header("💰 Investment Parameters")
        
        # Instruction text in BLACK (was red)
        st.markdown('<p class="instruction-text">Enter the price per share at which you purchased the stock:</p>', unsafe_allow_html=True)
        purchase_price_per_share = st.number_input(
            "Purchase Price per Share (PKR)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="purchase_price_per_share",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown('<p class="instruction-text">Enter the total amount you invested (number of shares × purchase price):</p>', unsafe_allow_html=True)
        total_purchase_price = st.number_input(
            "Total Purchase Price (PKR)",
            min_value=0.0,
            value=0.0,
            step=10000.0,
            key="total_purchase_price",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown('<p class="instruction-text">Enter your desired profit percentage on total investment (before tax and utilities):</p>', unsafe_allow_html=True)
        required_profit_percent = st.number_input(
            "Required Profit (%) - Excluding Tax & Utilities",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="required_profit_percent",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.header("💰 Tax & Utilities")
        
        st.markdown('<p class="instruction-text">Enter the Capital Gains Tax percentage that will be deducted from your profit:</p>', unsafe_allow_html=True)
        tax_rate = st.number_input(
            "Tax Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=1.0,
            key="tax_rate",
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="instruction-text">Enter the Brokerage + Utilities fees percentage:</p>', unsafe_allow_html=True)
        utilities_rate = st.number_input(
            "Utilities Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=1.0,
            key="utilities_rate",
            label_visibility="collapsed"
        )
        
        # Store values
        if purchase_price_per_share > 0:
            predictor.purchase_price_per_share = purchase_price_per_share
        if total_purchase_price > 0:
            predictor.total_purchase_price = total_purchase_price
        if required_profit_percent > 0:
            predictor.required_profit_percent = required_profit_percent
        predictor.tax_rate = tax_rate
        predictor.utilities_rate = utilities_rate
        
        st.markdown("---")
        
        if st.button("🔍 Analyze Stock", use_container_width=True):
            with st.spinner("Fetching real-time data..."):
                predictor.current_stock = stock_symbol
                symbol = predictor.psx_stocks[stock_symbol]['symbol']
                predictor.data = predictor.fetch_stock_data(symbol, period)
                
                if predictor.data:
                    st.session_state.analyzed = True
                    st.success("✅ Data loaded successfully!")
                    st.rerun()
                else:
                    st.error("Failed to load data. Please try another stock.")
    
    # Main content
    if st.session_state.analyzed and predictor.data:
        stock_info = predictor.psx_stocks[predictor.current_stock]
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Current Price", f"PKR {predictor.data['current_price']:,.2f}")
        with col2:
            st.metric("Market Cap", predictor.data['market_cap'])
        with col3:
            st.metric("P/E Ratio", predictor.data['pe_ratio'])
        with col4:
            st.metric("Dividend Yield", f"{predictor.data['dividend_yield']}%")
        with col5:
            st.metric("Volatility", f"{predictor.data['volatility']}%")
        
        # Enhanced Profit/Loss Calculation
        if predictor.purchase_price_per_share and predictor.purchase_price_per_share > 0:
            current_price = predictor.data['current_price']
            profit_per_share_before_tax = current_price - predictor.purchase_price_per_share
            profit_percent_before_tax = (profit_per_share_before_tax / predictor.purchase_price_per_share) * 100
            
            # Calculate tax and utilities on profit
            if profit_per_share_before_tax > 0:
                tax_amount = profit_per_share_before_tax * (predictor.tax_rate / 100)
                utilities_amount = profit_per_share_before_tax * (predictor.utilities_rate / 100)
                profit_per_share_after_tax = profit_per_share_before_tax - tax_amount - utilities_amount
                profit_percent_after_tax = (profit_per_share_after_tax / predictor.purchase_price_per_share) * 100
            else:
                tax_amount = 0
                utilities_amount = 0
                profit_per_share_after_tax = profit_per_share_before_tax
                profit_percent_after_tax = profit_percent_before_tax
            
            # Calculate shares and total investment
            if predictor.total_purchase_price > 0:
                shares = predictor.total_purchase_price / predictor.purchase_price_per_share
                total_investment = predictor.total_purchase_price
                total_profit_before_tax = profit_per_share_before_tax * shares
                total_profit_after_tax = profit_per_share_after_tax * shares
                current_value = shares * current_price
            else:
                shares = 0
                total_investment = 0
                total_profit_before_tax = 0
                total_profit_after_tax = 0
                current_value = 0
            
            # Required analysis based on profit percentage
            if predictor.required_profit_percent > 0:
                required_profit_amount = total_investment * (predictor.required_profit_percent / 100)
                required_profit_per_share = required_profit_amount / shares if shares > 0 else 0
                required_price_before_tax = predictor.purchase_price_per_share + required_profit_per_share
                
                # Calculate required price after tax
                required_profit_after_tax = required_profit_per_share
                required_profit_before_tax_calc = required_profit_after_tax / (1 - (predictor.tax_rate + predictor.utilities_rate) / 100)
                required_price_after_tax = predictor.purchase_price_per_share + required_profit_before_tax_calc
                
                price_gap_before_tax = required_price_before_tax - current_price
                price_gap_after_tax = required_price_after_tax - current_price
                
                required_status_before = "✅ Achievable" if current_price >= required_price_before_tax else "❌ Not Yet"
                required_status_after = "✅ Achievable" if current_price >= required_price_after_tax else "❌ Not Yet"
                
                # Check if profit target achieved
                profit_target_achieved = profit_percent_before_tax >= predictor.required_profit_percent
            else:
                required_profit_amount = 0
                required_profit_per_share = 0
                required_price_before_tax = 0
                required_price_after_tax = 0
                price_gap_before_tax = 0
                price_gap_after_tax = 0
                required_status_before = "Not Set"
                required_status_after = "Not Set"
                profit_target_achieved = False
            
            # HOLD/SELL Recommendation based on profit percentage achievement
            recommendation = ""
            recommendation_color = ""
            recommendation_reason = ""
            
            if predictor.required_profit_percent > 0:
                if profit_target_achieved:
                    recommendation = "✅ SELL - Target Profit Achieved!"
                    recommendation_color = "success"
                    recommendation_reason = f"Your profit of {profit_percent_before_tax:.1f}% has met/exceeded your target of {predictor.required_profit_percent:.1f}%"
                elif profit_percent_before_tax > 0:
                    remaining_percent = predictor.required_profit_percent - profit_percent_before_tax
                    recommendation = "⚠️ HOLD - Profit Not Yet at Target"
                    recommendation_color = "warning"
                    recommendation_reason = f"You have achieved {profit_percent_before_tax:.1f}% profit, need {remaining_percent:.1f}% more to reach target"
                else:
                    recommendation = "🔴 HOLD - Currently at Loss"
                    recommendation_color = "error"
                    recommendation_reason = f"You are at a loss of {abs(profit_percent_before_tax):.1f}%. Wait for price to recover before considering sell"
            else:
                if profit_percent_before_tax > 0:
                    recommendation = "✅ PROFIT OPPORTUNITY - Consider Selling"
                    recommendation_color = "success"
                    recommendation_reason = f"You are currently at {profit_percent_before_tax:.1f}% profit"
                else:
                    recommendation = "📊 MONITOR - Currently at Loss"
                    recommendation_color = "info"
                    recommendation_reason = f"You are at a loss of {abs(profit_percent_before_tax):.1f}%. Monitor the stock for recovery"
            
            # Display comprehensive portfolio status
            st.info(f"""
            **📈 PORTFOLIO STATUS**
            
            **Purchase Details:**
            - Purchase Price per Share: PKR {predictor.purchase_price_per_share:,.2f}
            - Total Investment: PKR {total_investment:,.2f}
            - Number of Shares: {shares:,.0f}
            
            **Current Status (Before Tax):**
            - Current Price: PKR {current_price:,.2f}
            - Profit/Loss per Share: PKR {profit_per_share_before_tax:+.2f} ({profit_percent_before_tax:+.1f}%)
            - Total Profit/Loss: PKR {total_profit_before_tax:+,.2f}
            - Current Portfolio Value: PKR {current_value:,.2f}
            
            **After Tax & Utilities ({predictor.tax_rate}% Tax + {predictor.utilities_rate}% Fees):**
            - Tax Amount: PKR {tax_amount:,.2f} per share
            - Utilities/Fees: PKR {utilities_amount:,.2f} per share
            - Net Profit per Share: PKR {profit_per_share_after_tax:+.2f} ({profit_percent_after_tax:+.1f}%)
            - Net Total Profit: PKR {total_profit_after_tax:+,.2f}
            
            **Required Profit Analysis ({predictor.required_profit_percent:.1f}% target on total investment):**
            - Required Profit Amount: PKR {required_profit_amount:,.2f}
            - Required Profit per Share: PKR {required_profit_per_share:,.2f}
            - Required Price (Before Tax): PKR {required_price_before_tax:,.2f} - {required_status_before}
            - Required Price (After Tax): PKR {required_price_after_tax:,.2f} - {required_status_after}
            - Gap to Target (Before Tax): PKR {price_gap_before_tax:+.2f}
            - Gap to Target (After Tax): PKR {price_gap_after_tax:+.2f}
            """)
            
            # Display recommendation prominently
            if recommendation_color == "success":
                st.success(f"### {recommendation}")
                st.success(f"**Recommendation:** {recommendation_reason}")
                st.success(f"**If you sell NOW:** You will make {profit_percent_before_tax:.1f}% profit (PKR {total_profit_before_tax:+,.2f} before tax)")
            elif recommendation_color == "warning":
                st.warning(f"### {recommendation}")
                st.warning(f"**Recommendation:** {recommendation_reason}")
                st.warning(f"**If you sell NOW:** You will make {profit_percent_before_tax:.1f}% profit (PKR {total_profit_before_tax:+,.2f} before tax)")
            elif recommendation_color == "error":
                st.error(f"### {recommendation}")
                st.error(f"**Recommendation:** {recommendation_reason}")
                st.error(f"**If you sell NOW:** You will incur a loss of {abs(profit_percent_before_tax):.1f}% (PKR {total_profit_before_tax:+,.2f} before tax)")
            else:
                st.info(f"### {recommendation}")
                st.info(f"**Recommendation:** {recommendation_reason}")
                st.info(f"**If you sell NOW:** {profit_percent_before_tax:+.1f}% return (PKR {total_profit_before_tax:+,.2f} before tax)")
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📈 Price Chart", "📊 Technical Analysis", "🎯 Predictions"])
        
        with tab1:
            st.subheader(f"{predictor.current_stock} - Price Chart")
            
            df = pd.DataFrame({
                'Date': predictor.data['dates'],
                'Price': predictor.data['prices'],
                'Volume': predictor.data['volumes']
            })
            
            fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])
            
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['Price'], mode='lines', name='Price',
                          line=dict(color='#FFD700', width=2)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='#667eea'),
                row=2, col=1
            )
            
            fig.update_layout(template='plotly_dark', height=600, showlegend=True)
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Price (PKR)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Technical Indicators")
            
            tech = predictor.calculate_technical_indicators(predictor.data['prices'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RSI (14)", tech['RSI'],
                         delta="Overbought" if tech['RSI'] > 70 else ("Oversold" if tech['RSI'] < 30 else "Neutral"))
            with col2:
                st.metric("MA (20)", f"PKR {tech['MA20']:,.2f}")
                st.metric("MA (50)", f"PKR {tech['MA50']:,.2f}")
            with col3:
                st.metric("Bollinger Upper", f"PKR {tech['Upper Band']:,.2f}")
                st.metric("Bollinger Lower", f"PKR {tech['Lower Band']:,.2f}")
            
            st.subheader("Historical Data")
            hist_df = pd.DataFrame({
                'Date': predictor.data['dates'][-20:],
                'Open': predictor.data['open'][-20:],
                'High': predictor.data['high'][-20:],
                'Low': predictor.data['low'][-20:],
                'Close': predictor.data['prices'][-20:],
                'Volume': predictor.data['volumes'][-20:]
            })
            st.dataframe(hist_df, use_container_width=True)
        
        with tab3:
            st.subheader("5-Month Price Predictions")
            
            predictions, lower, upper = predictor.predict_future()
            months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5"]
            
            pred_df = pd.DataFrame({
                'Month': months,
                'Predicted Price': [f"PKR {p:,.2f}" for p in predictions],
                'Lower Bound': [f"PKR {l:,.2f}" for l in lower],
                'Upper Bound': [f"PKR {u:,.2f}" for u in upper]
            })
            st.dataframe(pred_df, use_container_width=True)
            
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=months, y=predictions, mode='lines+markers',
                name='Predicted', line=dict(color='#FFD700', width=2)
            ))
            fig_pred.add_trace(go.Scatter(
                x=months, y=upper, mode='lines',
                name='Upper Bound', line=dict(color='gray', dash='dash')
            ))
            fig_pred.add_trace(go.Scatter(
                x=months, y=lower, mode='lines',
                name='Lower Bound', line=dict(color='gray', dash='dash')
            ))
            fig_pred.update_layout(template='plotly_dark', height=500)
            st.plotly_chart(fig_pred, use_container_width=True)
            
            expected_return = ((predictions[-1] - predictor.data['current_price']) / predictor.data['current_price']) * 100
            st.metric("Expected 5-Month Return", f"{expected_return:+.1f}%")
    
    else:
        st.info("👈 **Welcome!** Select a stock from the sidebar and click 'Analyze Stock' to begin.")
        
        st.markdown("""
        ### Features:
        - 📈 **Real-time price charts** with historical data
        - 📊 **Technical indicators** (RSI, Moving Averages, Bollinger Bands)
        - 💰 **Portfolio tracker** to calculate profit/loss
        - 🎯 **5-month price predictions** with confidence intervals
        - 📱 **Professional interface** with dark theme
        
        ### Available Sectors:
        - Banking, Cement, Fertilizer, Oil & Gas, Technology, Power
        """)

if __name__ == "__main__":
    main()