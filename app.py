import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Load and preprocess data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Stocks_2025.csv")
    df = df.drop("Unnamed: 0", axis=1)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Stock"] = df["Stock"].replace(" ", "", regex=True)
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()
    return df

# --- Load data ---
df = load_data()

# --- Streamlit UI ---
st.set_page_config(page_title="Nifty Stock Visualizer", layout="wide")
st.title("📈 Nifty Stock Visualizer with SMA, Volume & Filters")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Select Category
categories = df["Category"].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

# Filter Data by Category
df_category = df[df["Category"] == selected_category]

# Select Stock
stocks = df_category["Stock"].dropna().unique()
selected_s_
