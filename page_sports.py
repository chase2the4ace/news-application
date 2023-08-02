import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import requests
import webbrowser

language_codes = {
    "English": "en",
    "French": "fr",
    "Mandarin": "zh",
    "Spanish": "es"
}

def create_sports_page(window):

    sports_window = tk.Toplevel(window)
    sports_window.title("Sports News")
    sports_window.configure(bg="black")

    sports_label = tk.Label(sports_window, text="Sports News", bg="black", fg="white", font=("Arial", 16, "bold"))
    sports_label.pack(pady=10)

    sports_news_list = tk.Listbox(sports_window, bg="black", fg="white", selectbackground="gray", font=("Arial", 14))
    sports_news_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    query = "sports"
    selected_language = "English"
    language = language_codes.get(selected_language, "en")

    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy=publishedAt&apiKey=9df37fcf24514f6080060fc9f05ae437"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles'][:5]

        if articles:
            sports_news_list.delete(0, tk.END)

            for idx, article in enumerate(articles, start=1):
                title = article['title']
                published_at = article['publishedAt']
                description = article['description']
                sports_news_list.insert(tk.END, f"{idx}. {title}\nPublished At: {published_at}\n{description}\n\n")

        else:
            sports_news_list.insert(tk.END, "No sports articles found.\n")

    else:
        sports_news_list.insert(tk.END, "Error returning sports news. Please try again later.\n")

    def open_article(event):
        selected_index = sports_news_list.curselection()
        if selected_index:
            article_idx = selected_index[0]
            article_data = articles[article_idx]
            article_url = article_data.get('url', None)
            if article_url:
                webbrowser.open(article_url)

    sports_news_list.bind("<<ListboxSelect>>", open_article)