# NEPSE Stock Market Dashboard

An interactive dashboard for analyzing Nepal Stock Exchange (NEPSE) stock market data with comprehensive visualizations and insights.

## 📊 Features

### Interactive Dashboard
- **Market Trends**: Track daily trading volume and value over time
- **Sector Analysis**: Compare performance across different market sectors
- **Company Explorer**: Detailed analysis of individual companies with candlestick charts
- **Top Performers**: Identify top gainers, losers, and most traded stocks
- **Data Explorer**: Filter and download raw data

### Data Analysis
- Comprehensive statistical analysis of market data
- Sector-wise performance metrics
- Price movement tracking
- Volatility analysis
- Trading activity insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```powershell
   cd c:\Users\Asus\Development\nepse-dashboard-small
   ```

2. **Install required packages**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Dashboard

**Launch the interactive dashboard:**
```powershell
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Running Data Analysis

**Run the data analysis script:**
```powershell
python data_analysis.py
```

This will output comprehensive statistics including:
- Dataset overview
- Sector analysis
- Top companies by volume and value
- Price change analysis
- Trading activity trends
- Volatility metrics

## 📁 Project Structure

```
nepse-dashboard-small/
├── ALL_COMPANIES_COMPLETE.csv    # Stock market data
├── dashboard.py                   # Interactive Streamlit dashboard
├── data_analysis.py              # Data analysis script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 📈 Dashboard Features Explained

### 1. Market Trends
- View daily trading volume and value over time
- Filter by custom date ranges
- Interactive area and line charts

### 2. Sector Analysis
- Pie chart showing market share by trading value
- Bar chart of top sectors by volume
- Detailed sector statistics table

### 3. Company Explorer
- Select any company to view detailed analysis
- Candlestick price charts
- Trading volume visualization
- Performance metrics (price change, volume, value, trades)
- Recent trading data table

### 4. Top Performers
- Top 10 gainers with percentage change
- Top 10 losers with percentage change
- Top 15 companies by trading volume

### 5. Data Explorer
- Filter data by sector, company, and date
- View up to 1,000 most recent records
- Download filtered data as CSV

## 📊 Data Overview

The dataset includes:
- **84,946** total records
- Multiple companies across various sectors
- Date range from late 2024 to late 2025
- Fields: Symbol, CompanyName, Sector, Date, High, Low, Close, Volume, Value_NPR, Trades

### Sectors Included
- Commercial Banks
- Life Insurance
- And many more...

## 🛠️ Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Dashboard Capabilities
- Real-time filtering and interaction
- Responsive design
- Export functionality
- Caching for improved performance

## 💡 Usage Tips

1. **Start with Market Trends**: Get an overview of overall market activity
2. **Explore Sectors**: Identify which sectors are most active
3. **Dive into Companies**: Use Company Explorer for detailed analysis
4. **Track Performance**: Check Top Performers to find opportunities
5. **Export Data**: Use Data Explorer to download filtered datasets

## 🔧 Troubleshooting

**Dashboard won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**Port already in use:**
```powershell
streamlit run dashboard.py --server.port 8502
```

**Data not loading:**
- Ensure `ALL_COMPANIES_COMPLETE.csv` is in the same directory
- Check file permissions

## 📝 Customization

You can customize the dashboard by modifying `dashboard.py`:
- Change color schemes in the Plotly chart configurations
- Adjust the number of top performers shown
- Add new analysis tabs
- Modify date ranges and filters

## 🤝 Contributing

Feel free to enhance the dashboard by:
- Adding new visualizations
- Implementing additional metrics
- Improving performance
- Adding export formats

## 📄 License

This project is for educational and analytical purposes.

## 📧 Support

For questions or issues, please review the code documentation or check the inline comments in both `dashboard.py` and `data_analysis.py`.

---

**Enjoy exploring NEPSE market data! 📈**
