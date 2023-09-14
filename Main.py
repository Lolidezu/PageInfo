import requests
import time

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
    
url = input("Enter website url: ")
fixed_url = "https://" + url
load_time = get_page_load_time(fixed_url)
ttfb = get_ttfb(fixed_url)
if load_time:
    print(f"The page loaded in {load_time:.6f} seconds.")
else:
    print("Failed to fetch the page.")

if ttfb is not None:
    print(f"The page get first byte in {load_time:.6f} seconds.")
else:
    print("Failed to fetch the page.")