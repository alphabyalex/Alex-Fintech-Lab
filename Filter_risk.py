import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox, Text

# Function to apply criteria and get top assets
def get_top_assets(results, num_assets):
    try:
        # Filter results based on criteria
        filtered_results = results[
            (results['Avg Return'] >= 0.11) &
            (results['Expected Return'] >= 0.115) &
            (results['Beta'] < 2.35) &
            (results['20-Year Risk adj'].notnull())  # Ensure there's a 20-year risk adj value
        ]

        # If 'Market Cap' column exists, filter by market cap >= 200 million
        if 'Market Cap' in results.columns:
            filtered_results = filtered_results[
                (filtered_results['Market Cap'] >= 100000000)  # Exclude assets <= 200 million
            ]

        # Sort by 20-Year Risk adj in descending order
        sorted_results = filtered_results.sort_values(by='20-Year Risk adj', ascending=False)

        # Return the top assets based on user input
        return sorted_results.head(num_assets), len(filtered_results)

    except KeyError:
        messagebox.showerror("Error", "One or more columns are missing in the results data.")
        return pd.DataFrame(), 0  # Return an empty DataFrame and 0 count on error

# Function to read results from CSV file
def read_results_from_csv(filepath):
    try:
        results = pd.read_csv(filepath)
        return results
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filepath}' not found.")
        return None

# Function to display the top assets in a new window
def display_top_assets(results, count):
    # Create a new window
    top_assets_window = tk.Toplevel(root)
    top_assets_window.title("Top Assets")

    # Create a text widget to display the results
    text_widget = tk.Text(top_assets_window, wrap='none', padx=20, pady=20, font=("Courier", 10))
    text_widget.pack(fill='both', expand=True)

    # Add a scrollbar to the text widget
    scrollbar = tk.Scrollbar(top_assets_window, command=text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    text_widget['yscrollcommand'] = scrollbar.set

    # Format the result text
    result_text = f"{count} assets met the criteria.\n\n"
    result_text += "Ticker\tAvg Return\tExpected Return\tBeta\t20-Year Return\tSector\n"
    for _, asset in results.iterrows():
        result_text += f"{asset['Ticker']}\t{asset['Avg Return'] * 100:.2f}%\t{asset['Expected Return'] * 100:.2f}%\t{asset['Beta']:.2f}\t{asset['20-Year Risk adj'] * 100:.2f}%\t{asset['Sector']}\n"

    # Insert the result text into the text widget
    text_widget.insert('1.0', result_text)

    # Button to copy results to clipboard
    def copy_to_clipboard():
        top_assets_window.clipboard_clear()
        top_assets_window.clipboard_append(result_text)
        top_assets_window.update()  # Ensure clipboard content is updated
        messagebox.showinfo("Copy to Clipboard", "Top assets data copied to clipboard.")

    copy_button = tk.Button(top_assets_window, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

# Main function to process the results and display top assets
def main():
    global root
    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Read results from CSV file
    results = read_results_from_csv("asset_results.csv")
    if results is not None:
        try:
            # Ask user for the number of top assets to display
            num_assets = simpledialog.askinteger("Input", "Enter the number of top assets you would like to display:", minvalue=1)
            if num_assets is not None:
                # Get top assets based on criteria
                top_assets, count = get_top_assets(results, num_assets)
                if not top_assets.empty:
                    # Display the top assets
                    display_top_assets(top_assets, count)
                else:
                    messagebox.showinfo("Result", "No assets met the criteria.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    root.mainloop()

if __name__ == "__main__":
    main()
