import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Load and preprocess data ---
@st.cache_data
def load_data():
    df = pd.read_csv("../Datasets/Nifty/Stocks_2025.csv")
    
    # Drop unnamed index column if it exists
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)
    
    # Safely parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])  # Drop rows where date couldn't be parsed

    # Clean stock names
    df["Stock"] = df["Stock"].replace(" ", "", regex=True)

    # Calculate moving averages
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

    return df

# --- Load data ---
df = load_data()

# --- Streamlit Page Setup ---
st.set_page_config(page_title="📈 Nifty Stock Visualizer", layout="wide")
st.title("📈 Nifty Stock Visualizer with SMA, Volume & Filters")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Select Category
categories = df["Category"].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter by category
df_category = df[df["Category"] == selected_category]

# Select Stock
stocks = df_category["Stock"].dropna().unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks))

# Filter by stock
df_stock = df_category[df_category["Stock"] == selected_stock]

# Select Date Range
min_date = df_stock["Date"].min()
max_date = df_stock["Date"].max()

date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply date range filter
df_stock = df_stock[(df_stock["Date"] >= pd.to_datetime(date_range[0])) & (df_stock["Date"] <= pd.to_datetime(date_range[1]))]

# SMA Toggles
show_sma_50 = st.sidebar.checkbox("Show SMA 50", value=True)
show_sma_200 = st.sidebar.checkbox("Show SMA 200", value=True)

# Volume Toggle
show_volume = st.sidebar.checkbox("Show Volume Chart", value=False)

# --- Plot Chart ---
st.subheader(f"📊 Price Chart for {selected_stock}")

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot Close price
sns.lineplot(data=df_stock, x="Date", y="Close", label="Close", ax=ax1, marker='o')

# Plot SMAs
if show_sma_50:
    sns.lineplot(data=df_stock, x="Date", y="SMA_50", label="SMA 50", ax=ax1)
if show_sma_200:
    sns.lineplot(data=df_stock, x="Date", y="SMA_200", label="SMA 200", ax=ax1)

# Format
ax1.set_xlabel("Date")
ax1.set_ylabel("Price")
ax1.set_title(f"{selected_stock} Stock Price with SMA")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
ax1.legend(loc='upper left')

# Plot Volume
if show_volume and "Volume" in df_stock.columns:
    ax2 = ax1.twinx()
    sns.barplot(data=df_stock, x="Date", y="Volume", color="skyblue", alpha=0.3, ax=ax2)
    ax2.set_ylabel("Volume")
    ax2.grid(False)

# Show plot
st.pyplot(fig)

# --- Data Download ---
st.markdown("### 📥 Download Filtered Data")
csv_data = df_stock.to_csv(index=False)
st.download_button("Download CSV", data=csv_data, file_name=f"{selected_stock}_data.csv", mime='text/csv')

# --- Raw Data Table ---
with st.expander("📄 Show Raw Data Table"):
    st.dataframe(df_stock.reset_index(drop=True), use_container_width=True)

   
