import tkinter as tk
from tkinter import filedialog
import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

class ReviewAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Review Data Analysis Tool")
        
        self.load_button = tk.Button(self.root, text="Load Review Data", command=self.load_review_data)
        self.load_button.pack(pady=10)
        
        self.analyze_button = tk.Button(self.root, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.pack(pady=10)
        
        self.download_button = tk.Button(self.root, text="Download Analyzed CSV", command=self.download_csv)
        self.download_button.pack(pady=10)
        
        self.result_text = tk.Text(self.root, wrap=tk.WORD)
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.review_data = None
        self.original_size = 0
        self.deduplicated_size = 0
    
    def load_review_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.review_data = pd.read_csv(file_path)
            self.original_size = os.path.getsize(file_path)
            self.result_text.insert(tk.END, "Review data loaded successfully.\n")
    
    def analyze_data(self):
        if self.review_data is not None:
            self.deduplicated_size = len(self.review_data.to_csv(index=False))
            
            average_rating = self.calculate_average_rating(self.review_data)
            self.result_text.insert(tk.END, f"Average Rating: {average_rating:.2f}\n")
            
            self.review_data = self.perform_sentiment_analysis(self.review_data)
            most_common_positive, most_common_negative = self.identify_frequent_keywords(self.review_data, top_n=5)
            
            self.result_text.insert(tk.END, "Most Common Positive Keywords:\n")
            for keyword, count in most_common_positive:
                self.result_text.insert(tk.END, f"{keyword}: {count}\n")
            
            self.result_text.insert(tk.END, "Most Common Negative Keywords:\n")
            for keyword, count in most_common_negative:
                self.result_text.insert(tk.END, f"{keyword}: {count}\n")
            
            size_reduction = (1 - self.deduplicated_size / self.original_size) * 100
            self.result_text.insert(tk.END, f"Size reduction: {size_reduction:.2f}%\n")
            
            similarity_index = self.calculate_similarity_index(self.review_data)
            self.result_text.insert(tk.END, f"Similarity Index: {similarity_index:.2f}\n")
        else:
            self.result_text.insert(tk.END, "Please load review data first.\n")
    
    
    def calculate_average_rating(self, data):
        return data['rating'].mean()
    
    def perform_sentiment_analysis(self, data):
        data['sentiment'] = data['review_text'].apply(lambda text: TextBlob(text).sentiment.polarity)
        return data
    
    def identify_frequent_keywords(self, data, top_n=5):
        positive_keywords = Counter()
        negative_keywords = Counter()
        
        for index, row in data.iterrows():
            text = row['review_text']
            sentiment = row['sentiment']
            
            if sentiment > 0:
                positive_keywords.update(text.split())
            elif sentiment < 0:
                negative_keywords.update(text.split())
        
        most_common_positive = positive_keywords.most_common(top_n)
        most_common_negative = negative_keywords.most_common(top_n)
        
        return most_common_positive, most_common_negative
    
    def download_csv(self):
        if self.review_data is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if save_path:
                self.review_data.to_csv(save_path, index=False)
                self.result_text.insert(tk.END, "Analyzed CSV file downloaded successfully.\n")
        else:
            self.result_text.insert(tk.END, "Please load and analyze data before downloading.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReviewAnalysisApp(root)
    root.mainloop()
