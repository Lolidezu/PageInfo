from urllib.parse import urljoin
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
    
def get_resource_size(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return len(response.content)
    except requests.RequestException:
        return None
        
def get_img_size(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img')
            img_urls = [urljoin(url, img['src']) for img in img_tags if 'src' in img.attrs]
            img_sizes = [size for size in (get_resource_size(img_url) for img_url in img_urls) if size is not None]
            return sum(img_sizes)/(1024*1024)
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
    
def get_vid_size(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            video_tags = soup.find_all('video')
            vid_urls = [urljoin(url, video['src']) for video in video_tags if 'src' in video.attrs]
            vid_sizes = [size for size in (get_resource_size(vid_url) for vid_url in vid_urls) if size is not None]
            return sum(vid_sizes)/(1024*1024)
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
        imgSize = get_img_size(fixed_url)
        vidSize = get_vid_size(fixed_url)

        if title:
            st.write(f"The page [ {title} ] data is")
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
        if imageCount is not None and imageCount != 0:
            st.write(f"The page has : {imageCount} images.")
            st.write(f"The images total size are : {imgSize:.2f} megabytes.")
        if videoCount is not None and videoCount != 0:
            st.write(f"The page has : {videoCount} videos.")
            st.write(f"The videos total size are : {vidSize:.2f} megabytes.")
        else:
            st.write("Other info of the page is not available or unloadable.")

if __name__ == "__main__":
    main()
