from tkinter import font
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from tkinter import *
import requests
import time

def get_website_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.title.string
    except:
        return None

def get_page_load_time(url):
    start_time = time.time()
    
    try:
        response = requests.get(url)
        end_time = time.time()

        if response.status_code == 200:
            load_time = end_time - start_time
            return load_time
        else:
            return None
    except requests.RequestException:
        print(f"Failed to fetch {url}")
        return None

def get_ttfb(url):
    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
        
        start_time = time.time()
        response.iter_content(1)
        end_time = time.time()
        
        ttfb = end_time - start_time
        return ttfb
    
def get_page_size(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            size_in_bytes = len(response.content)
            size_in_kilobytes = size_in_bytes / 1024
            return size_in_kilobytes
    except requests.RequestException:
        return None

from bs4 import BeautifulSoup

def get_text_amount(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.stripped_strings
            text_length = sum(len(item) for item in text)
            return text_length
    except requests.RequestException:
        return None
    
def get_image_count(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            images = soup.find_all('img')
            image_count = len(images) 
            return image_count
    except requests.RequestException:
        return None

def get_video_count(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = soup.find_all('video')
            video_count = len(videos)
            return video_count
    except requests.RequestException:
        return None
    
def fetch_data():
    url = url_entry.get()
    fixed_url = "https://" + url

    load_time = get_page_load_time(fixed_url)
    ttfb = get_ttfb(fixed_url)
    title = get_website_title(fixed_url)
    pageSize = get_page_size(fixed_url)
    imageCount = get_image_count(fixed_url)
    videoCount = get_video_count(fixed_url)
    
    result_text.delete(1.0, "end")
    if title is not None:
        result_text.insert("end", "The page : " + title + " data is\n")
    if load_time:
        result_text.insert("end", f"The page loaded in {load_time:.6f} seconds.\n")
    if ttfb is not None:
        result_text.insert("end", f"The page get first byte in {ttfb:.6f} seconds.\n")
    if pageSize is not None:
        result_text.insert("end", f"The page size is : {pageSize:.6f} kilobytes.\n")
    if imageCount is not None:
        result_text.insert("end", "The page have : " + str(imageCount) + " images.\n")
    if videoCount is not None:
        result_text.insert("end", "The page have : " + str(videoCount) + " videos.\n")        
    else:
        result_text.insert("end", "Failed to fetch the page.\n")
    

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


app = Tk()
app.title("Website Info Fetcher")
app.geometry("1280x720")

custom_font = font.Font(family="Arial", size=12)
url_label = Label(app, text="Enter website url:", font=custom_font)
url_label.pack(pady=10)

url_entry = Entry(app, width=40, font=custom_font)
url_entry.pack(pady=10)

button_image = PhotoImage(file="button_image.png")
fetch_button = ttk.Button(app, command=fetch_data, image=button_image, compound="left")
fetch_button.pack(pady=10)

text_frame = Frame(app)
text_frame.pack(pady=10)

# Adjust the Text widget to be a child of the frame
result_text = Text(text_frame, height=10, width=40, wrap='word', font=custom_font)
result_text.pack(side='left', fill='both', expand=True)

# Adjust the Scrollbar to be a child of the frame and bind it to the Text widget
scrollbar = Scrollbar(text_frame, command=result_text.yview)
scrollbar.pack(side='right', fill='y')
result_text.config(yscrollcommand=scrollbar.set)

app.mainloop()

"""    
url = input("Enter website url: ")
fixed_url = "https://" + url
load_time = get_page_load_time(fixed_url)
ttfb = get_ttfb(fixed_url)
title = get_website_title(fixed_url)
if title is not None:
    print("The page : " + title + " data is")
if load_time:
    print(f"The page loaded in {load_time:.6f} seconds.")
else:
    print("Failed to fetch the page.")

if ttfb is not None:
    print(f"The page get first byte in {load_time:.6f} seconds.")
else:
    print("Failed to fetch the page.")
"""