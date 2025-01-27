import requests
import time
import os

# Replace this with your Render app's URL
url = os.environ.get("RENDER_APP_URL")  # Add your app's URL here

while True:
    try:
        # Send a GET request to your web app to keep it alive
        response = requests.get(url)
        print(f"Request sent, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

    # Wait for 15 seconds before sending the next request
    time.sleep(15)
