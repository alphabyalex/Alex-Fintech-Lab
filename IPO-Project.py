# ipo_analysis_ui.py

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import pyperclip  # pip install pyperclip

# --- Placeholder Data Fetcher (replace with real API later) ---
def fetch_ipo_financials(ticker):
    """
    Fetch IPO data (dummy version).
    Replace with SEC Edgar or financial API later.
    """
    return {
        'ticker': ticker,
        'debt': np.random.randint(50, 500),  # in millions
        'revenue_growth_ttm': np.random.uniform(-0.2, 0.5),  # %
        'revenue_growth_yoy': np.random.uniform(-0.2, 0.6),  # %
        'net_income_ytd': np.random.randint(-100, 200),  # in millions
        'net_income_last_year': np.random.randint(-150, 250),  # in millions
    }

# --- Format financial data ---
def format_financials(financials):
    profitability = "Profitable ✅" if financials['net_income_ytd'] > 0 else "Unprofitable ❌"
    return f"""
Ticker: {financials['ticker']}
Current Debt: ${financials['debt']}M
Revenue Growth (TTM): {financials['revenue_growth_ttm']*100:.2f}%
Revenue Growth (This Year): {financials['revenue_growth_yoy']*100:.2f}%
Net Income YTD: ${financials['net_income_ytd']}M
Net Income Last Year: ${financials['net_income_last_year']}M
Status: {profitability}
"""

# --- UI Window ---
def analyze_ticker():
    ticker = ticker_entry.get().strip().upper()
    if not ticker:
        messagebox.showwarning("Input Error", "Please enter a ticker.")
        return
    
    financials = fetch_ipo_financials(ticker)
    output = format_financials(financials)
    
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, output)

def copy_to_clipboard():
    content = text_box.get(1.0, tk.END).strip()
    pyperclip.copy(content)
    messagebox.showinfo("Copied", "Data copied to clipboard!")

# --- Main Window ---
root = tk.Tk()
root.title("IPO Analysis Tool")
root.geometry("500x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter IPO Ticker:").grid(row=0, column=0, padx=5)
ticker_entry = tk.Entry(frame, width=15)
ticker_entry.grid(row=0, column=1, padx=5)

analyze_btn = tk.Button(frame, text="Analyze", command=analyze_ticker)
analyze_btn.grid(row=0, column=2, padx=5)

text_box = tk.Text(root, wrap="word", height=15, width=60)
text_box.pack(pady=10)

copy_btn = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_btn.pack()

root.mainloop()
