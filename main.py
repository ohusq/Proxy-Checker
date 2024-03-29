import threading
import requests
import time
import sys
from queue import Queue
from precheck import check_permissions

# Use a thread-safe queue for storing working proxies
working_proxies_queue = Queue()

def check_proxy(proxy, google_pass):
    try:
        delta_time = time.time() # current time
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            delta_time = time.time() - delta_time
            delta_time = round(delta_time, 2) * 1000
            print(f"Proxy {proxy} is working @ {int(delta_time)}ms")
            with open("working.txt", "a") as f:
                f.write(f"{proxy}\n")
            working_proxies_queue.put(proxy)  # Add proxy to the thread-safe queue
            if google_pass and "Our systems have detected unusual traffic" in response.text:
                print(f"Google is blocked by proxy {proxy}")
                with open("google_blocked_proxies.txt", "a") as f:
                    f.write(f"{proxy}\n")
    except requests.exceptions.SSLError:
        # Handle SSL certificate verification failures silently
        pass
    except requests.exceptions.Timeout:
        # Handle timeout errors silently
        pass
    except requests.exceptions.ConnectionError:
        # Handle connection errors silently
        pass
    except requests.exceptions.RequestException as e:
        # Handle all other requests exceptions silently
        pass
    except Exception as e:
        # Print other types of exceptions
        print(f"Error occurred with proxy {proxy}: {e}")

def print_ascii_art():
    with open("ascii.txt", 'r') as file:
        ascii_art = file.read()
        print(ascii_art)

def main():
    checklist = ["working.txt", "google_blocked_proxies.txt", "ascii.txt", sys.argv[1]]
    for file in checklist:
        if not check_permissions(file):
            exit(1)

    try:
        file_path = sys.argv[1]
        google_pass = bool(sys.argv[2]) if len(sys.argv) > 2 else True  # Google pass option (optional, boolean)
        if file_path is None:
            print("Usage: python main.py <file_path> <google_pass : boolean | default=True>")
            exit(1)
    except IndexError:
        print("Usage: python main.py <file_path> <google_pass : boolean | default=True>")
        exit(1)

    print_ascii_art()
    
    
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    total_proxies = len(proxies)
    print(f"Checking {total_proxies} proxies...")
    start_time = time.time()
    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=(proxy, google_pass))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Finished checking {total_proxies} proxies @ {int(round(time.time() - start_time, 2)*1000)}ms")

if __name__ == "__main__":
    main()
