import requests
from src.sportsradar.simulation.config import Config


def create_session(url: str, recording_id: str):
    """
    Creates a session for the given recording ID.

    :param url: The URL to send the POST request to.
    :param recording_id: The ID of the recording.
    :return: The response from the API, or None if the request failed.
    """
    headers = {
        "Content-Type": f"application/{Config.CONTENT_TYPE}",
    }

    json_data = {
        "query": "mutation CreateSession($input: CreateSessionInput!) {\n createSession(input: $input)\n }",
        "variables": {
            "input": {
                "recordingId": recording_id,
            },
        },
    }

    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()  # Will only proceed if the request was successful
    except requests.RequestException as e:
        print(f"Request failed with {e}")
        return None

    return response


# Usage
# url = 'https://playback.sportradar.com/graphql'
# recording_id = '50d7e8f3-a1ce-4fcf-bb15-f8a2ad919e34'
# response = create_session(url, recording_id)
