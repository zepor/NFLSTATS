import json
import os
from threading import Thread
import src.utils.log as be_logger
from security import safe_requests

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))
# Set your Sportradar API key here
api_key = os.getenv('APIKEY')

# Define the URLs for the different push feeds
feeds = {
    "draft_picks": "https://api.sportradar.com/draft/nfl/trial/stream/en/picks/subscribe",
    "draft_trades": "https://api.sportradar.com/draft/nfl/trial/stream/en/trades/subscribe",
    "events": "https://api.sportradar.com/nfl/official/trial/stream/en/events/subscribe",
    "pulse": "https://api.sportradar.com/nfl/official/trial/stream/en/pulse/subscribe",
    "statistics": "https://api.sportradar.com/nfl/official/trial/stream/en/statistics/subscribe",
}

# Function to handle the subscription and be_logger.infoing of data@log_and_catch_exceptions
def subscribe_to_feed(feed_url, params):
    while True:
        with safe_requests.get(feed_url, params=params, allow_redirects=False, stream=True) as r:
            if r.status_code == 200:
                redirect_url = r.headers['Location']
                be_logger.info(f"Listening for data on {feed_url}")
                with safe_requests.get(redirect_url, stream=True) as stream:
                    for line in stream.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            data = json.loads(decoded_line)
                            be_logger.info(json.loads(decoded_line))
                be_logger.info(f"Terminated connection to {feed_url}")
            else:
                be_logger.info(f"Failed to subscribe to feed: {feed_url}, HTTP Status Code: {r.status_code}")
        be_logger.info(f"Starting subscription to {feed_name}")
        subscribe_to_feed(url, params)

def start_feed_subscription(feed_name, url, params):
    print(f"Starting subscription to {feed_name}")
    subscribe_to_feed(url, params)
# Start the subscription to each feed in a separate threaddef start_subscriptions(api_key):
def start_subscriptions(api_key):
    threads = []
    for feed_name, url in feeds.items():
        feed_thread = Thread(target=start_feed_subscription, args=(feed_name, url, {'api_key': api_key}))
        feed_thread.daemon = True
        feed_thread.start()
        threads.append(feed_thread)
    return threads  # Return the list of threads

if __name__ == '__main__':
    if not api_key:
        raise ValueError("APIKEY environment variable not set")
    threads = start_subscriptions(api_key)

    # Keep the main thread running to keep the subscription threads alive
    for thread in threads:
        thread.join()
