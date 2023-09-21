import requests
from bs4 import BeautifulSoup
import requests
import time
import streamlit as st
import socket

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
    start_time = time.perf_counter()
    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
        
        # Consume the first byte
        next(response.iter_content(1))
        end_time = time.perf_counter()
        
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

def get_dns_resolution_time(domain):
    start_time = time.perf_counter()
    try:
        ip_address = socket.gethostbyname(domain)
        end_time = time.perf_counter()
        return end_time - start_time
    except socket.gaierror:
        return None

def get_connection_time(domain, port):
    try:
        ip_address = socket.gethostbyname(domain)
        start_time = time.perf_counter()
        
        with socket.create_connection((ip_address, port), timeout=10) as s:  # timeout is set to 10 seconds.
            end_time = time.perf_counter()
        
        return end_time - start_time
    except (socket.timeout, socket.error):
        return None


#The web page | | |
#             V V V

def main():
    st.title("Website Info Fetcher")

    url = st.text_input("Enter website url:")

    if st.button("Check"):
        fixed_url = "https://" + url

        load_time = get_page_load_time(fixed_url)
        ttfb = get_ttfb(fixed_url)
        connect_time = get_connection_time(url,443)
        title = get_website_title(fixed_url)
        pageSize = get_page_size(fixed_url)
        imageCount = get_image_count(fixed_url)
        videoCount = get_video_count(fixed_url)
        dns = get_dns_resolution_time(url)

        if title:
            st.write(f"The page : {title} data is")
        if load_time:
            st.write(f"The page loaded in {load_time * 1000:.2f} milliseconds.")
        if ttfb:
            st.write(f"The page get first byte in {ttfb * 1000:.2f} milliseconds.")
        if dns is not None:
            st.write(f"The page DNS is {dns * 1000:.2f} milliseconds.")
        if connect_time is not None:
            st.write(f"The page connection time is {connect_time * 1000:.2f} milliseconds.")
        if pageSize:
            st.write(f"The page size is : {pageSize:.6f} kilobytes.")
        if imageCount is not None:
            st.write(f"The page has : {imageCount} images.")
        if videoCount is not None:
            st.write(f"The page has : {videoCount} videos.")
        else:
            st.write("Failed to fetch other info of the page.")

if __name__ == "__main__":
    main()
