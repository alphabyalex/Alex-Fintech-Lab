import pandas as pd
import tkinter as tk
from tkinter import ttk
import yfinance as yf
import csv

# Global cancel flag
cancel_flag = False

# Function to get stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max", auto_adjust=True)
    return hist['Close']

# Function to get beta
def get_beta(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('beta')

# Function to calculate expected return using CAPM
def calculate_expected_return(beta, risk_free_rate=0.045, market_return=0.102):
    return risk_free_rate + beta * (market_return - risk_free_rate)

# Function to get average return over the last 10 years from Yahoo Finance
def get_average_return_yahoo(ticker, years=10):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max", auto_adjust=True)
    trading_days = 252 * years
    if len(hist) >= trading_days:
        close_prices = hist['Close'][-trading_days:]
        total_return = (close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]
        avg_return_yahoo = (1 + total_return) ** (1 / years) - 1
        return avg_return_yahoo
    elif len(hist) >= 7 * 252:  # fallback for 7+ years
        close_prices = hist['Close'][-7 * 252:]
        total_return = (close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]
        avg_return_yahoo = (1 + total_return) ** (1 / 7) - 1
        return avg_return_yahoo
    else:
        return None

# Function to calculate 20-year return based on expected return
def calculate_20_year_return(expected_return):
    return (1 + expected_return) ** 20 - 1

# Function to calculate 20-year risk-adjusted return
def calculate_20_year_risk_adj(expected_return, beta):
    return (calculate_20_year_return(expected_return) - (1.045) ** 20) / beta

# Function to get sector of the stock
def get_sector(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('sector')

# Function to get market capitalization
def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get('marketCap')

# Function to calculate metrics for all assets
def calculate_metrics_for_all_assets(tickers, progress_var, root):
    results = []
    total_tickers = len(tickers)
    for idx, ticker in enumerate(tickers):
        if cancel_flag:
            print("Process canceled by user.")
            break
        try:
            avg_return_yahoo = get_average_return_yahoo(ticker)
            if avg_return_yahoo is not None:
                beta = get_beta(ticker)
                if beta is not None:
                    exp_return = calculate_expected_return(beta)
                    market_cap = get_market_cap(ticker)
                    sector = get_sector(ticker)
                    return_20_year = calculate_20_year_return(exp_return)
                    risk_adj_20_year_return = calculate_20_year_risk_adj(exp_return, beta)
                    results.append((ticker, avg_return_yahoo, exp_return, beta, return_20_year,
                                    risk_adj_20_year_return, market_cap, sector))
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")

        progress_var.set((idx + 1) / total_tickers * 100)
        root.update_idletasks()  # Update the GUI to show progress

    return results

# Function to read tickers from a plain text file
def read_tickers_from_file(filepath):
    try:
        with open(filepath, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
        return tickers
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []

# Function to save results to CSV file
def save_results_to_csv(results, filepath):
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Ticker', 'Avg Return', 'Expected Return', 'Beta',
                      '20-Year Risk adj', 'Market Cap', 'Sector']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            try:
                writer.writerow({
                    'Ticker': result[0],
                    'Avg Return': result[1],
                    'Expected Return': result[2],
                    'Beta': result[3],
                    '20-Year Risk adj': result[5],
                    'Market Cap': result[6],
                    'Sector': result[7]
                })
            except IndexError:
                print(f"Error: Incomplete data for {result[0]}. Skipping.")

# Function to cancel the process
def cancel_process():
    global cancel_flag
    cancel_flag = True

# Function to process tickers and save results with a progress bar
def process_with_progress_bar(root):
    tickers = read_tickers_from_file("assetlistall")  # Plain text file
    if tickers:
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
        progress_bar.pack(pady=20)

        cancel_button = tk.Button(root, text="Cancel", command=cancel_process)
        cancel_button.pack(pady=10)

        def start_processing():
            results = calculate_metrics_for_all_assets(tickers, progress_var, root)
            save_results_to_csv(results, "asset_results.csv")
            print("Results saved to 'asset_results.csv'.")
            root.quit()

        root.after(100, start_processing)
        root.mainloop()

# Create the main window
root = tk.Tk()
root.title("Processing Tickers")
root.geometry("500x150")
root.eval('tk::PlaceWindow . center')

if __name__ == "__main__":
    process_with_progress_bar(root)
