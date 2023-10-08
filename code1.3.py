import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

# Load CSV files into DataFrames
calendar_data = pd.read_csv('calendar_dec18.csv')
listings_data = pd.read_csv('listings_dec18.csv')
reviews_data = pd.read_csv('reviews_dec18.csv')

# Function to filter data based on user input
def search_data(keyword):
    filtered_data = listings_data[listings_data.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]
    return filtered_data

# Function to generate a price distribution chart
def generate_price_distribution_chart(suburb):
    filtered_data = listings_data[listings_data['suburb'] == suburb]
    plt.hist(filtered_data['price'], bins=10, edgecolor='black')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Price Distribution for Suburb: {}'.format(suburb))
    plt.show()

# Function to analyze cleanliness comments
def analyze_cleanliness_comments():
    cleanliness_keywords = ['clean', 'hygiene', 'tidy', 'neat']
    cleanliness_comments = reviews_data[reviews_data['comments'].apply(lambda x: any(keyword in str(x).lower() for keyword in cleanliness_keywords))]
    num_cleanliness_comments = len(cleanliness_comments)
    return num_cleanliness_comments

# Function to handle the search button
def search_button_click():
    keyword = search_entry.get()
    filtered_data = search_data(keyword)
    display_data(filtered_data)

# Function to handle the chart button
def chart_button_click():
    suburb = suburb_entry.get()
    generate_price_distribution_chart(suburb)

# Function to handle the cleanliness analysis button
def cleanliness_button_click():
    num_comments = analyze_cleanliness_comments()
    messagebox.showinfo("Cleanliness Analysis", f"Number of comments related to cleanliness: {num_comments}")

# Function to handle the date selection
def date_selection():
    start_date = calendar_start_date.get()
    end_date = calendar_end_date.get()

    # Filter data based on the selected date range
    filtered_data = calendar_data[(calendar_data['date'] >= start_date) & (calendar_data['date'] <= end_date)]
    display_data(filtered_data)

# Function to display data in a table with scrollable view
def display_data(data):
    # Create a new window to display the data
    data_window = tk.Toplevel(root)
    data_window.title("Display Data")
    data_window.geometry("800x400")

    # Create a scrolled text widget with vertical and horizontal scrolling
    scroll_text = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=80, height=20, xscrollcommand=True, yscrollcommand=True)
    scroll_text.pack(expand=True, fill='both')

    # Insert the data into the scrollable text widget
    scroll_text.insert(tk.END, data.to_string(index=False))

# Create the main application window
root = tk.Tk()
root.title("Real Estate Analyzer")
root.geometry("800x600")

# Search bar
search_label = tk.Label(root, text="Enter keyword:")
search_label.pack(pady=10)
search_entry = tk.Entry(root)
search_entry.pack(pady=5)
search_button = tk.Button(root, text="Search", command=search_button_click)
search_button.pack(pady=5)

# Suburb entry for chart
suburb_label = tk.Label(root, text="Enter suburb:")
suburb_label.pack(pady=10)
suburb_entry = tk.Entry(root)
suburb_entry.pack(pady=5)
chart_button = tk.Button(root, text="Generate Chart", command=chart_button_click)
chart_button.pack(pady=5)

# Cleanliness analysis button
cleanliness_button = tk.Button(root, text="Cleanliness Analysis", command=cleanliness_button_click)
cleanliness_button.pack(pady=5)

# Date selection
date_label = tk.Label(root, text="Select Date Range:")
date_label.pack(pady=10)
calendar_start_label = tk.Label(root, text="Start Date:")
calendar_start_label.pack(pady=5)
calendar_start_date = tk.Entry(root)
calendar_start_date.pack(pady=5)
calendar_end_label = tk.Label(root, text="End Date:")
calendar_end_label.pack(pady=5)
calendar_end_date = tk.Entry(root)
calendar_end_date.pack(pady=5)
date_select_button = tk.Button(root, text="Select Date Range", command=date_selection)
date_select_button.pack(pady=5)

# Run the main event loop
root.mainloop()
