import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Load and preprocess data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Stocks_2025.csv")
    
    # Drop unnamed index column if it exists
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)
    
    # Safely parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])  # Drop rows where date couldn't be parsed

    # Clean stock names
    df["Stock"] = df["Stock"].replace(" ", "", regex=True)

    # Calculate moving averages
    df["SMA_50"] = df["C]()_]()
