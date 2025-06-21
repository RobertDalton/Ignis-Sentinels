import requests

def fetch_with_params(base_url: str, params: dict = None, headers: dict = None):
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        response = requests.post(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except:
        return {}
