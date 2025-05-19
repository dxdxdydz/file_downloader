import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# URL of the main directory
base_url = 'https://dl.ibdocs.re/IB%20BOOKS/Group%204%20-%20Sciences/Chemistry/'

# Directory to save the downloaded files
download_dir = 'D:/IB/Chemistry Book'

# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Function to get all file links and subdirectory links inside <li> with class="item folder"
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    file_links = []
    subdir_links = []

    # Find all <li> elements with class "item folder"
    for li in soup.find_all(class_='fb-n'):
        # Inside each <li>, find the <a> tag with the href attribute
        link = li.find('a', href=True)
        if link:
            href = link['href']
            full_url = urljoin(url, href)  # Convert relative URL to absolute URL
            
            # Check if the link is a file (ends with common file extensions)
            if href.endswith(('.pdf', '.zip', '.tar', '.rar', '.txt', '.docx', 'xlsx','pptx')):  
                file_links.append(full_url)
            # Check if it's a subdirectory (ends with a '/')
            elif href.endswith('/'):
                subdir_links.append(full_url)

    return file_links, subdir_links

# Function to download a file from a URL
def download_file(url, save_path):
    print(f'Downloading {url} to {save_path}')
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

# Function to recursively download files and handle subdirectories
def download_all_files(url, current_dir):
    print(f'Accessing {url}')
    file_links, subdir_links = get_links(url)

    # Download all files in the current directory
    for file_url in file_links:
        file_name = os.path.basename(file_url)
        save_path = os.path.join(current_dir, file_name)
        download_file(file_url, save_path)

    # Recursively access and download files from subdirectories
    for subdir_url in subdir_links:
        subdir_name = os.path.basename(urlparse(subdir_url).path.strip('/'))
        subdir_path = os.path.join(current_dir, subdir_name)

        # Create subdirectory if it doesn't exist
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

        # Recursively download files in the subdirectory
        download_all_files(subdir_url, subdir_path)

# Main function to start the download
def start_download():
    download_all_files(base_url, download_dir)
    print('All files downloaded!')

if __name__ == '__main__':
    start_download()

