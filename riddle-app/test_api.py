import requests

def test_riddle_api():
    try:
        response = requests.get("https://riddles-api.vercel.app/random")
        response.raise_for_status()  # Raise an error for bad responses
        riddles = response.json()
        print("Fetched riddles:", riddles)  # Print the fetched riddles
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  # Log connection errors
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")  # Log timeout errors
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception: {req_err}")  # Log general request errors
    except Exception as e:
        print(f"General error: {e}")  # Log any other exceptions

if __name__ == "__main__":
    test_riddle_api()

