# src/downloader.py

import requests

def download_tiktok_video(url):
    """
    Download TikTok video from the given URL.
    
    Args:
        url (str): The URL of the TikTok video to download.
    
    Returns:
        str: The direct video URL if successful, None otherwise.
    """
    try:
        # Example API endpoint (replace with actual API logic)
        api_url = f'https://api.tikwm.com/video?url={url}'  # Hypothetical API endpoint
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            video_url = data.get('video_url')  # Adjust based on actual API response
            return video_url
        else:
            print(f"Error: Received status code {response.status_code} from the API.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
