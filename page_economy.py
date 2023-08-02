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

def create_economics_page(window):

    economics_window = tk.Toplevel(window)
    economics_window.title("Economics News")
    economics_window.configure(bg="black")

    economics_label = tk.Label(economics_window, text="Economics News", bg="black", fg="white", font=("Arial", 16, "bold"))
    economics_label.pack(pady=10)

    economics_news_list = tk.Listbox(economics_window, bg="black", fg="white", selectbackground="gray", font=("Arial", 14))
    economics_news_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    query = "economics"
    selected_language = "English"
    language = language_codes.get(selected_language, "en")

    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy=publishedAt&apiKey=9df37fcf24514f6080060fc9f05ae437"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles'][:5]

        if articles:
            economics_news_list.delete(0, tk.END)

            for idx, article in enumerate(articles, start=1):
                title = article['title']
                published_at = article['publishedAt']
                description = article['description']
                economics_news_list.insert(tk.END, f"{idx}. {title}\nPublished At: {published_at}\n{description}\n\n")

        else:
            economics_news_list.insert(tk.END, "No economics articles found.\n")

    else:
        economics_news_list.insert(tk.END, "Error returning economics news. Please try again later.\n")

    def open_article(event):
        selected_index = economics_news_list.curselection()
        if selected_index:
            article_idx = selected_index[0]
            article_data = articles[article_idx]
            article_url = article_data.get('url', None)
            if article_url:
                webbrowser.open(article_url)

    economics_news_list.bind("<<ListboxSelect>>", open_article)
