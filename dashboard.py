"""
NEPSE Stock Market Dashboard
Interactive dashboard for exploring Nepal Stock Exchange data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="NEPSE Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and prepare data"""
    df = pd.read_csv('ALL_COMPANIES_COMPLETE.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def create_market_overview(df):
    """Create market overview section"""
    st.markdown('<div class="main-header">📈 NEPSE Stock Market Dashboard</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Companies",
            value=f"{df['Symbol'].nunique():,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Sectors",
            value=f"{df['Sector'].nunique()}",
            delta=None
        )
    
    with col3:
        total_volume = df['Volume'].sum()
        st.metric(
            label="Total Volume Traded",
            value=f"{total_volume/1e6:.1f}M",
            delta=None
        )
    
    with col4:
        total_value = df['Value_NPR'].sum()
        st.metric(
            label="Total Value (NPR)",
            value=f"{total_value/1e9:.2f}B",
            delta=None
        )
    
    st.markdown("---")

def market_trends_tab(df):
    """Market trends visualization"""
    st.header("📊 Market Trends")
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=df['Date'].min(),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=df['Date'].max(),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
    
    # Filter data
    mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
    filtered_df = df[mask]
    
    # Daily market activity
    daily_stats = filtered_df.groupby('Date').agg({
        'Volume': 'sum',
        'Value_NPR': 'sum',
        'Trades': 'sum'
    }).reset_index()
    
    # Volume over time
    fig_volume = px.area(
        daily_stats,
        x='Date',
        y='Volume',
        title='Daily Trading Volume',
        labels={'Volume': 'Total Volume', 'Date': 'Date'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_volume.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig_volume, width='stretch')
    
    # Value traded over time
    fig_value = px.line(
        daily_stats,
        x='Date',
        y='Value_NPR',
        title='Daily Trading Value (NPR)',
        labels={'Value_NPR': 'Total Value (NPR)', 'Date': 'Date'},
        color_discrete_sequence=['#2ca02c']
    )
    fig_value.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig_value, width='stretch')

def sector_analysis_tab(df):
    """Sector analysis visualization"""
    st.header("🏢 Sector Analysis")
    
    # Sector statistics
    sector_stats = df.groupby('Sector').agg({
        'Symbol': 'nunique',
        'Volume': 'sum',
        'Value_NPR': 'sum',
        'Trades': 'sum'
    }).reset_index()
    
    sector_stats.columns = ['Sector', 'Companies', 'Volume', 'Value_NPR', 'Trades']
    sector_stats = sector_stats.sort_values('Value_NPR', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sector by value pie chart
        fig_pie = px.pie(
            sector_stats,
            values='Value_NPR',
            names='Sector',
            title='Market Share by Trading Value',
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, width='stretch')
    
    with col2:
        # Sector by volume bar chart
        fig_bar = px.bar(
            sector_stats.head(10),
            x='Volume',
            y='Sector',
            orientation='h',
            title='Top 10 Sectors by Trading Volume',
            color='Volume',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, width='stretch')
    
    # Sector statistics table
    st.subheader("Sector Statistics")
    display_df = sector_stats.copy()
    display_df['Value_NPR'] = display_df['Value_NPR'].apply(lambda x: f"NPR {x:,.0f}")
    display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:,}")
    display_df['Trades'] = display_df['Trades'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, width='stretch', hide_index=True)

def company_explorer_tab(df):
    """Company explorer with detailed analysis"""
    st.header("🔍 Company Explorer")
    
    # Company selector
    companies = sorted(df['Symbol'].unique())
    selected_company = st.selectbox("Select a Company", companies)
    
    if selected_company:
        company_df = df[df['Symbol'] == selected_company].sort_values('Date')
        company_info = company_df.iloc[0]
        
        # Company info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Company:** {company_info['CompanyName']}")
        with col2:
            st.info(f"**Sector:** {company_info['Sector']}")
        with col3:
            latest_price = company_df.iloc[-1]['Close']
            st.info(f"**Latest Price:** NPR {latest_price:,.2f}")
        
        # Price performance
        col1, col2 = st.columns(2)
        
        with col1:
            # Price chart
            fig_price = go.Figure()
            
            fig_price.add_trace(go.Candlestick(
                x=company_df['Date'],
                open=company_df['Close'],  # Using Close as open for simplicity
                high=company_df['High'],
                low=company_df['Low'],
                close=company_df['Close'],
                name='Price'
            ))
            
            fig_price.update_layout(
                title=f'{selected_company} Price Chart',
                yaxis_title='Price (NPR)',
                xaxis_title='Date',
                height=400,
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig_price, width='stretch')
        
        with col2:
            # Volume chart
            fig_volume = px.bar(
                company_df,
                x='Date',
                y='Volume',
                title=f'{selected_company} Trading Volume',
                labels={'Volume': 'Volume', 'Date': 'Date'},
                color='Volume',
                color_continuous_scale='Viridis'
            )
            fig_volume.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_volume, width='stretch')
        
        # Performance metrics
        st.subheader("Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        first_price = company_df.iloc[0]['Close']
        last_price = company_df.iloc[-1]['Close']
        price_change_pct = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0
        
        with col1:
            st.metric("Price Change", f"{price_change_pct:+.2f}%", delta=f"{last_price - first_price:+.2f}")
        with col2:
            st.metric("Total Volume", f"{company_df['Volume'].sum():,}")
        with col3:
            st.metric("Total Value", f"NPR {company_df['Value_NPR'].sum():,.0f}")
        with col4:
            st.metric("Total Trades", f"{company_df['Trades'].sum():,}")
        
        # Recent trading data
        st.subheader("Recent Trading Data")
        recent_df = company_df.tail(10)[['Date', 'High', 'Low', 'Close', 'Volume', 'Value_NPR', 'Trades']].copy()
        recent_df['Date'] = recent_df['Date'].dt.strftime('%Y-%m-%d')
        recent_df = recent_df.sort_values('Date', ascending=False)
        st.dataframe(recent_df, width='stretch', hide_index=True)

def top_performers_tab(df):
    """Top and bottom performers"""
    st.header("🏆 Top Performers")
    
    # Calculate performance for each company
    df_sorted = df.sort_values(['Symbol', 'Date'])
    first_prices = df_sorted.groupby('Symbol').first()[['Close', 'Date', 'CompanyName', 'Sector']]
    last_prices = df_sorted.groupby('Symbol').last()[['Close', 'Date']]
    
    performance = pd.DataFrame({
        'Company': first_prices['CompanyName'],
        'Sector': first_prices['Sector'],
        'First_Price': first_prices['Close'],
        'Last_Price': last_prices['Close']
    })
    
    performance['Change_Pct'] = ((performance['Last_Price'] - performance['First_Price']) / 
                                  performance['First_Price'] * 100)
    performance = performance[performance['First_Price'] > 0]  # Filter out invalid data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Top Gainers")
        top_gainers = performance.nlargest(10, 'Change_Pct').reset_index(names='Symbol')
        top_gainers['Change_Pct'] = top_gainers['Change_Pct'].apply(lambda x: f"+{x:.2f}%")
        top_gainers['First_Price'] = top_gainers['First_Price'].apply(lambda x: f"{x:.2f}")
        top_gainers['Last_Price'] = top_gainers['Last_Price'].apply(lambda x: f"{x:.2f}")
        st.dataframe(
            top_gainers[['Symbol', 'Company', 'Sector', 'First_Price', 'Last_Price', 'Change_Pct']],
            width='stretch',
            hide_index=True
        )
    
    with col2:
        st.subheader("📉 Top Losers")
        top_losers = performance.nsmallest(10, 'Change_Pct').reset_index(names='Symbol')
        top_losers['Change_Pct'] = top_losers['Change_Pct'].apply(lambda x: f"{x:.2f}%")
        top_losers['First_Price'] = top_losers['First_Price'].apply(lambda x: f"{x:.2f}")
        top_losers['Last_Price'] = top_losers['Last_Price'].apply(lambda x: f"{x:.2f}")
        st.dataframe(
            top_losers[['Symbol', 'Company', 'Sector', 'First_Price', 'Last_Price', 'Change_Pct']],
            width='stretch',
            hide_index=True
        )
    
    # Top by volume
    st.subheader("📊 Top by Trading Volume")
    top_volume = df.groupby(['Symbol', 'CompanyName', 'Sector']).agg({
        'Volume': 'sum',
        'Value_NPR': 'sum'
    }).reset_index().sort_values('Volume', ascending=False).head(15)
    
    fig_top_volume = px.bar(
        top_volume,
        x='Volume',
        y='Symbol',
        orientation='h',
        title='Top 15 Companies by Trading Volume',
        color='Volume',
        color_continuous_scale='Teal',
        hover_data=['CompanyName', 'Sector']
    )
    fig_top_volume.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_top_volume, width='stretch')

def data_explorer_tab(df):
    """Raw data explorer"""
    st.header("📋 Data Explorer")
    
    st.write(f"Dataset contains {len(df):,} records")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sectors = ['All'] + sorted(df['Sector'].unique().tolist())
        selected_sector = st.selectbox("Filter by Sector", sectors)
    
    with col2:
        companies = ['All'] + sorted(df['Symbol'].unique().tolist())
        selected_symbol = st.selectbox("Filter by Company", companies)
    
    with col3:
        date_filter = st.date_input(
            "Filter by Date (optional)",
            value=None
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_sector != 'All':
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
    
    if selected_symbol != 'All':
        filtered_df = filtered_df[filtered_df['Symbol'] == selected_symbol]
    
    if date_filter:
        filtered_df = filtered_df[filtered_df['Date'] == pd.to_datetime(date_filter)]
    
    st.write(f"Showing {len(filtered_df):,} records")
    
    # Display data
    display_df = filtered_df.sort_values('Date', ascending=False).head(1000)
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(display_df, width='stretch', height=600)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name=f"nepse_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def main():
    """Main dashboard function"""
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    # Market overview
    create_market_overview(df)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Market Trends",
        "🏢 Sector Analysis",
        "🔍 Company Explorer",
        "🏆 Top Performers",
        "📋 Data Explorer"
    ])
    
    with tab1:
        market_trends_tab(df)
    
    with tab2:
        sector_analysis_tab(df)
    
    with tab3:
        company_explorer_tab(df)
    
    with tab4:
        top_performers_tab(df)
    
    with tab5:
        data_explorer_tab(df)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>NEPSE Stock Market Dashboard | Data updated through December 2025</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
