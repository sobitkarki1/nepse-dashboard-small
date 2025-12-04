"""
NEPSE Stock Market Data Analysis
Analyzes stock market data from NEPSE (Nepal Stock Exchange)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(filepath='ALL_COMPANIES_COMPLETE.csv'):
    """Load and clean the dataset"""
    print("Loading data...")
    df = pd.read_csv(filepath)
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Basic info
    print(f"\n{'='*60}")
    print(f"DATASET OVERVIEW")
    print(f"{'='*60}")
    print(f"Total Records: {len(df):,}")
    print(f"Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"Number of Companies: {df['Symbol'].nunique()}")
    print(f"Number of Sectors: {df['Sector'].nunique()}")
    
    return df

def sector_analysis(df):
    """Analyze data by sector"""
    print(f"\n{'='*60}")
    print(f"SECTOR ANALYSIS")
    print(f"{'='*60}")
    
    sector_stats = df.groupby('Sector').agg({
        'Symbol': 'nunique',
        'Volume': 'sum',
        'Value_NPR': 'sum',
        'Trades': 'sum',
        'Close': 'mean'
    }).round(2)
    
    sector_stats.columns = ['Companies', 'Total Volume', 'Total Value (NPR)', 'Total Trades', 'Avg Close Price']
    sector_stats = sector_stats.sort_values('Total Value (NPR)', ascending=False)
    
    print("\nSector Statistics:")
    print(sector_stats.to_string())
    
    return sector_stats

def top_companies_analysis(df):
    """Analyze top companies by various metrics"""
    print(f"\n{'='*60}")
    print(f"TOP COMPANIES ANALYSIS")
    print(f"{'='*60}")
    
    # Get most recent date for each company
    latest_data = df.sort_values('Date').groupby('Symbol').tail(1)
    
    # Top by trading volume
    top_volume = df.groupby(['Symbol', 'CompanyName', 'Sector'])['Volume'].sum().reset_index()
    top_volume = top_volume.sort_values('Volume', ascending=False).head(10)
    
    print("\nTop 10 Companies by Trading Volume:")
    for idx, row in top_volume.iterrows():
        print(f"{row['Symbol']:15} | {row['CompanyName'][:40]:40} | {row['Volume']:,}")
    
    # Top by value traded
    top_value = df.groupby(['Symbol', 'CompanyName', 'Sector'])['Value_NPR'].sum().reset_index()
    top_value = top_value.sort_values('Value_NPR', ascending=False).head(10)
    
    print("\nTop 10 Companies by Trading Value (NPR):")
    for idx, row in top_value.iterrows():
        print(f"{row['Symbol']:15} | {row['CompanyName'][:40]:40} | {row['Value_NPR']:,.0f}")
    
    return top_volume, top_value

def price_analysis(df):
    """Analyze price movements"""
    print(f"\n{'='*60}")
    print(f"PRICE ANALYSIS")
    print(f"{'='*60}")
    
    # Calculate price changes for companies with sufficient data
    df_sorted = df.sort_values(['Symbol', 'Date'])
    
    # Get first and last price for each company
    first_prices = df_sorted.groupby('Symbol').first()[['Close', 'Date']]
    last_prices = df_sorted.groupby('Symbol').last()[['Close', 'Date']]
    
    price_change = pd.DataFrame({
        'First_Price': first_prices['Close'],
        'Last_Price': last_prices['Close'],
        'First_Date': first_prices['Date'],
        'Last_Date': last_prices['Date']
    })
    
    price_change['Change_Pct'] = ((price_change['Last_Price'] - price_change['First_Price']) / 
                                   price_change['First_Price'] * 100)
    
    # Top gainers
    top_gainers = price_change.nlargest(10, 'Change_Pct')
    print("\nTop 10 Gainers (% Change):")
    for symbol, row in top_gainers.iterrows():
        print(f"{symbol:15} | {row['First_Price']:8.2f} → {row['Last_Price']:8.2f} | +{row['Change_Pct']:.2f}%")
    
    # Top losers
    top_losers = price_change.nsmallest(10, 'Change_Pct')
    print("\nTop 10 Losers (% Change):")
    for symbol, row in top_losers.iterrows():
        print(f"{symbol:15} | {row['First_Price']:8.2f} → {row['Last_Price']:8.2f} | {row['Change_Pct']:.2f}%")
    
    return price_change

def trading_activity_analysis(df):
    """Analyze trading activity over time"""
    print(f"\n{'='*60}")
    print(f"TRADING ACTIVITY ANALYSIS")
    print(f"{'='*60}")
    
    # Daily market statistics
    daily_stats = df.groupby('Date').agg({
        'Volume': 'sum',
        'Value_NPR': 'sum',
        'Trades': 'sum',
        'Symbol': 'nunique'
    })
    
    daily_stats.columns = ['Total Volume', 'Total Value (NPR)', 'Total Trades', 'Active Companies']
    
    print("\nOverall Trading Statistics:")
    print(f"Average Daily Volume: {daily_stats['Total Volume'].mean():,.0f}")
    print(f"Average Daily Value: NPR {daily_stats['Total Value (NPR)'].mean():,.0f}")
    print(f"Average Daily Trades: {daily_stats['Total Trades'].mean():,.0f}")
    print(f"Peak Trading Day (by value): {daily_stats['Total Value (NPR)'].idxmax().strftime('%Y-%m-%d')}")
    print(f"Peak Trading Value: NPR {daily_stats['Total Value (NPR)'].max():,.0f}")
    
    # Monthly trends
    monthly_stats = df.copy()
    monthly_stats['YearMonth'] = monthly_stats['Date'].dt.to_period('M')
    monthly_agg = monthly_stats.groupby('YearMonth').agg({
        'Volume': 'sum',
        'Value_NPR': 'sum',
        'Trades': 'sum'
    })
    
    print(f"\nMost Active Month: {monthly_agg['Value_NPR'].idxmax()}")
    print(f"Trading Value that Month: NPR {monthly_agg['Value_NPR'].max():,.0f}")
    
    return daily_stats, monthly_agg

def volatility_analysis(df):
    """Analyze price volatility"""
    print(f"\n{'='*60}")
    print(f"VOLATILITY ANALYSIS")
    print(f"{'='*60}")
    
    # Calculate daily volatility for each company
    df_with_range = df.copy()
    df_with_range['Daily_Range_Pct'] = ((df_with_range['High'] - df_with_range['Low']) / 
                                          df_with_range['Close'] * 100)
    
    # Filter out rows with zero or very low prices to avoid distortion
    df_filtered = df_with_range[df_with_range['Close'] > 10]
    
    volatility = df_filtered.groupby(['Symbol', 'CompanyName', 'Sector']).agg({
        'Daily_Range_Pct': 'mean'
    }).reset_index()
    
    volatility.columns = ['Symbol', 'CompanyName', 'Sector', 'Avg_Daily_Volatility']
    volatility = volatility.sort_values('Avg_Daily_Volatility', ascending=False)
    
    print("\nMost Volatile Companies (Top 10):")
    for idx, row in volatility.head(10).iterrows():
        print(f"{row['Symbol']:15} | {row['CompanyName'][:40]:40} | {row['Avg_Daily_Volatility']:.2f}%")
    
    print("\nLeast Volatile Companies (Top 10):")
    for idx, row in volatility.tail(10).iterrows():
        print(f"{row['Symbol']:15} | {row['CompanyName'][:40]:40} | {row['Avg_Daily_Volatility']:.2f}%")
    
    return volatility

def main():
    """Main analysis function"""
    print("\n" + "="*60)
    print("NEPSE STOCK MARKET DATA ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_and_clean_data()
    
    # Run analyses
    sector_stats = sector_analysis(df)
    top_volume, top_value = top_companies_analysis(df)
    price_change = price_analysis(df)
    daily_stats, monthly_agg = trading_activity_analysis(df)
    volatility = volatility_analysis(df)
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}\n")
    
    return {
        'df': df,
        'sector_stats': sector_stats,
        'top_volume': top_volume,
        'top_value': top_value,
        'price_change': price_change,
        'daily_stats': daily_stats,
        'monthly_agg': monthly_agg,
        'volatility': volatility
    }

if __name__ == "__main__":
    results = main()
