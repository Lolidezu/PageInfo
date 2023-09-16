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
