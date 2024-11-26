import requests
import os

def download_image(url, folder_path, file_name):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Full path for saving the image
    file_path = os.path.join(folder_path, file_name)

    # Download the image
    try:
        # Download the image
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

