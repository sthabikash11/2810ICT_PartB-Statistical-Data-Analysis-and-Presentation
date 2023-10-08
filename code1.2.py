import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PropertyAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Property Analyzer')
        self.root.geometry('800x600')

        self.setup_widgets()

    def setup_widgets(self):
        self.load_csv_button = ttk.Button(self.root, text='Load CSV', command=self.load_csv)
        self.load_csv_button.pack(pady=10)

        self.search_label = ttk.Label(self.root, text='Search:')
        self.search_label.pack()
        self.search_entry = ttk.Entry(self.root, width=30)
        self.search_entry.pack()

        self.search_button = ttk.Button(self.root, text='Search', command=self.search_data)
        self.search_button.pack(pady=10)

        self.graph_button = ttk.Button(self.root, text='Display Price Distribution', command=self.display_price_distribution)
        self.graph_button.pack(pady=10)

        self.period_label = ttk.Label(self.root, text='Select a period (YYYY-MM-DD):')
        self.period_label.pack()
        self.start_date_entry = ttk.Entry(self.root, width=12)
        self.start_date_entry.pack()
        self.end_date_entry = ttk.Entry(self.root, width=12)
        self.end_date_entry.pack()

        self.suburb_label = ttk.Label(self.root, text='Suburb:')
        self.suburb_label.pack()
        self.suburb_entry = ttk.Entry(self.root, width=15)
        self.suburb_entry.pack()

        self.report_button = ttk.Button(self.root, text='Report Listings', command=self.report_listings)
        self.report_button.pack(pady=10)

        self.keyword_label = ttk.Label(self.root, text='Keyword:')
        self.keyword_label.pack()
        self.keyword_entry = ttk.Entry(self.root, width=15)
        self.keyword_entry.pack()

        self.retrieve_button = ttk.Button(self.root, text='Retrieve Records', command=self.retrieve_records_by_keyword)
        self.retrieve_button.pack(pady=10)

        self.comments_button = ttk.Button(self.root, text='Analyze Cleanliness Comments', command=self.analyze_cleanliness_comments)
        self.comments_button.pack(pady=10)

    def load_csv(self):
        file_paths = filedialog.askopenfilenames(filetypes=[('CSV Files', '*.csv')])
        if file_paths:
            self.data = {}
            for file_path in file_paths:
                file_name = file_path.split('/')[-1]  # Extract the file name
                self.data[file_name] = pd.read_csv(file_path)
            print('CSV files loaded successfully.')

    def search_data(self):
        search_text = self.search_entry.get().lower()
        if hasattr(self, 'data'):
            matching_data = {}
            for file_name, df in self.data.items():
                matching_rows = df.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)
                matching_data[file_name] = df[matching_rows]
            self.display_data(matching_data)

    def display_data(self, data=None):
        if data is None:
            data = self.data
        if hasattr(self, 'data_frame'):
            self.data_frame.destroy()
        self.data_frame = ttk.Frame(self.root)
        self.data_frame.pack(pady=10)

        for file_name, df in data.items():
            label = ttk.Label(self.data_frame, text=f'Data from {file_name}')
            label.pack()
            tree = ttk.Treeview(self.data_frame)
            tree.pack()
            tree["columns"] = list(df.columns)
            for col in df.columns:
                tree.column(col, anchor='center')
                tree.heading(col, text=col)
            for index, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))

    def display_price_distribution(self):
        if hasattr(self, 'data') and 'listings_dec18.csv' in self.data and 'price' in self.data['listings_dec18.csv']:
            plt.figure(figsize=(6, 4))
            plt.hist(self.data['listings_dec18.csv']['price'], bins=20, edgecolor='black')
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.title('Price Distribution')

            if hasattr(self, 'graph_frame'):
                self.graph_frame.destroy()
            self.graph_frame = ttk.Frame(self.root)
            self.graph_frame.pack(pady=10)
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def report_listings(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        suburb = self.suburb_entry.get()

        if hasattr(self, 'data') and 'listings_dec18.csv' in self.data:
            listings_data = self.data['listings_dec18.csv'][(self.data['listings_dec18.csv']['date'] >= start_date) &
                                                             (self.data['listings_dec18.csv']['date'] <= end_date) &
                                                             (self.data['listings_dec18.csv']['suburb'] == suburb)]
            self.display_data({'Listings Data': listings_data})

    def retrieve_records_by_keyword(self):
        keyword = self.keyword_entry.get().lower()
        if hasattr(self, 'data'):
            matching_data = {}
            for file_name, df in self.data.items():
                if 'comments' in df:
                    matching_rows = df[df['comments'].str.lower().str.contains(keyword)]
                    matching_data[file_name] = matching_rows
            self.display_data(matching_data)

    def analyze_cleanliness_comments(self):
        if hasattr(self, 'data'):
            cleanliness_keywords = ['clean', 'tidy', 'hygiene']
            matching_data = {}
            for file_name, df in self.data.items():
                if 'comments' in df:
                    cleanliness_comments = df[df['comments'].str.contains('|'.join(cleanliness_keywords), case=False)]
                    matching_data[file_name] = cleanliness_comments
            self.display_data(matching_data)

# Create the main window
root = tk.Tk()
app = PropertyAnalyzerApp(root)
root.mainloop()
