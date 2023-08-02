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

def create_technology_page(window):

    technology_window = tk.Toplevel(window)
    technology_window.title("Technology News")
    technology_window.configure(bg="black")

    technology_label = tk.Label(technology_window, text="technology News", bg="black", fg="white", font=("Arial", 16, "bold"))
    technology_label.pack(pady=10)

    technology_news_list = tk.Listbox(technology_window, bg="black", fg="white", selectbackground="gray", font=("Arial", 14))
    technology_news_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    query = "technology"
    selected_language = "English"
    language = language_codes.get(selected_language, "en")

    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy=publishedAt&apiKey=9df37fcf24514f6080060fc9f05ae437"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles'][:5]

        if articles:
            technology_news_list.delete(0, tk.END)

            for idx, article in enumerate(articles, start=1):
                title = article['title']
                published_at = article['publishedAt']
                description = article['description']
                technology_news_list.insert(tk.END, f"{idx}. {title}\nPublished At: {published_at}\n{description}\n\n")

        else:
            technology_news_list.insert(tk.END, "No technology articles found.\n")

    else:
        technology_news_list.insert(tk.END, "Error returning technology news. Please try again later.\n")

    def open_article(event):
        selected_index = technology_news_list.curselection()
        if selected_index:
            article_idx = selected_index[0]
            article_data = articles[article_idx]
            article_url = article_data.get('url', None)
            if article_url:
                webbrowser.open(article_url)

    technology_news_list.bind("<<ListboxSelect>>", open_article)
