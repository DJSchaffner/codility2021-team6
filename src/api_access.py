import requests
import urllib
import sys

api_url ="https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod"

def query_live_data():
    response = _query_website(f"{api_url}/live-data")
    return response.json()

def query_building(interval: int, ts_start: int, ts_end: int):
    params = {"interval": interval, "begin-timestamp": ts_start, "end-timestamp": ts_end}
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    response = _query_website(f"{api_url}/building", params)

    return response.json()

def query_room(self, interval: int, ts_start: int, ts_end: int):
    params = {"interval": interval, "begin-timestamp": ts_start, "end-timestamp": ts_end}
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    
    response = _query_website(f"{api_url}/room", params)

    return response.json()

def _query_website(url: str, params: dict=None, ignore_success: bool=False):
    """Query a website with the given headers.

    Args:
        url (str): The url of the website to be queried
        params (dict, optional): The params to use. Defaults to None.
        ignore_success (bool, optional): If set to true, check if response is 200 and exit program if it is not. Defaults to False.

    Returns:
        requests.Response: The response of the request
    """
    response = requests.get(url, params=params)

    if (not ignore_success) and (not _is_response_successful(response)):
        _print_response_error(response)
        return None

    return response

def _is_response_successful(response: requests.Response):
    """Checks if a response returned successfully.

    Args:
        response (requests.Response): The response to check

    Returns:
        bool: True if successful (status code 200)
    """
    return response.status_code == 200

def _print_response_error(response: requests.Response):
    """Print the according error for a response.

    Args:
        response (requests.Response): The response containing the error code
    """
    print(f"Error in HTML request: {response.status_code} ({response.url}) => {response.json()['message']}")