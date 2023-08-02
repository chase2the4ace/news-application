import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import requests
from page_sports import create_sports_page
from page_politics import create_politics_page
from page_technology import create_technology_page
from page_economy import create_economics_page

#Will be used on all files for list of languages to choose from. Default language is English
language_codes = {
    "English": "en",
    "French": "fr",
    "Mandarin": "zh",
    "Spanish": "es"
}

def open_selected_page(event):
    selected_index = menu_listbox.curselection()
    if selected_index:
        selected_option = menu_listbox.get(selected_index[0])
        if selected_option == "Sports":
            open_sports_page()
        elif selected_option == "Politics":
            open_politics_page()
        elif selected_option == "Technology":
            open_technology_page()
        elif selected_option == "Economy":
            open_economics_page()

def open_technology_page():
    create_technology_page(window)

def open_sports_page():
    create_sports_page(window)

def open_politics_page():
    create_politics_page(window)

def open_economics_page():
    create_economics_page(window)

def search_news():
    query = search_entry.get()
    return_news(query)
def return_news(category):
    query = category
    selected_language = language_var.get()
    language = language_codes.get(selected_language, "en")

    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&sortBy=publishedAt&apiKey=9df37fcf24514f6080060fc9f05ae437"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles'][:5]

        if articles:
            news_list.delete(1.0, tk.END)

            for idx, article in enumerate(articles, start=1):
                title = article['title']
                published_at = article['publishedAt']
                description = article['description']
                image_url = article.get('urlToImage', None)

                news_list.insert(tk.END, f"{idx}. {title}\nPublished At: {published_at}\n{description}\n\n")

                if image_url:
                    image_data = requests.get(image_url, stream=True).raw
                    img = Image.open(image_data).resize((100, 100), Image.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                    image_label = tk.Label(news_list, image=img)
                    image_label.image = img
                    news_list.window_create(tk.END, window=image_label)
                    news_list.insert(tk.END, '\n')

        else:
            news_list.insert(tk.END, "No articles found.\n")

    else:
        news_list.insert(tk.END, "Error returning news. Please try again later.\n")

#Structuring the user interface
window = tk.Tk()
window.title("News Application")

title_bar = tk.Frame(window, bg="black", relief=tk.RAISED, bd=0)
title_bar.pack(fill=tk.X)

title_label = tk.Label(title_bar, text="News Application", fg="white", bg="black", font=("Arial", 16, "bold"))
title_label.pack(side=tk.LEFT, padx=10)

language_var = tk.StringVar(window)
language_var.set("English")
languages = ["English", "French", "Mandarin", "Spanish"]
language_menu = tk.OptionMenu(title_bar, language_var, *languages)
language_menu.config(bg="black", fg="white", relief=tk.FLAT)
language_menu.pack(side=tk.LEFT, padx=10)

def close_app():
    window.destroy()

exit_button = tk.Button(title_bar, text="Exit", command=close_app, bg="red", fg="white", relief=tk.FLAT)
exit_button.pack(side=tk.RIGHT, padx=0)

window.attributes('-fullscreen', True)
window.configure(bg="black")

menu_frame = tk.Frame(window, bg="white", width=200)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

menu_options = ["Sports", "Politics", "Economy", "Technology"]
menu_listbox = tk.Listbox(menu_frame, bg="white", selectbackground="gray", font=("Arial", 14))

for option in menu_options:
    menu_listbox.insert(tk.END, option)
    menu_listbox.pack(fill=tk.Y, padx=0, pady=40)

menu_listbox.bind("<<ListboxSelect>>", open_selected_page)

search_label = tk.Label(window, text="Enter your search query:", bg="black", fg="white")
search_label.pack(pady=10)
search_entry = tk.Entry(window)
search_entry.pack(pady=5)
search_entry.bind("<Return>", lambda event: search_news())

search_button = tk.Button(window, text="Search", command=lambda: return_news(search_entry.get()), bg="black", fg="white")
search_button.pack(pady=5)

news_list = scrolledtext.ScrolledText(window, width=80, height=20, bg="black", fg="white")
news_list.pack(pady=10)

window.mainloop()
