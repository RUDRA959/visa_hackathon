## NOT IN USE
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# Define credentials and URLs
client_id = '8xhnfmUlVHPdhYYLw6m3rD3UIDU4egH69bGw'
client_secret = 'ZTF8O94xdl1wVG7dJgpqxHYUzbhOCuo6TrZ2UB1qPSl1HNRR'
token_url = 'https://api.staging.ecolytiq.arm.ecolytiq.network/oauth/token'

# Dummy transactions
transactions = [
    {
        "Name": "transactions",
        "Value.accountId": "5a73582adf954cf6b3db6cc97bedccd9",
        "cluster_name_adjusted": "Affluent Segment",
        "Value.amount.currencyCode": "GBP",
        "mrch_catg_rlup_nm2": "AMUSEMENT PARKS/CIRCUS",
        "Value.dates.booked": "5/12/2023",
        "amount": 3.73,
        "Category": "entertainment"
    },
    {
        "Name": "transactions",
        "Value.accountId": "5a73582adf954cf6b3db6cc97bedccd9",
        "cluster_name_adjusted": "Affluent Segment",
        "Value.amount.currencyCode": "GBP",
        "mrch_catg_rlup_nm2": "AMUSEMENT PARKS/CIRCUS",
        "Value.dates.booked": "5/12/2023",
        "amount": 3.73,
        "Category": "entertainment"
    },
    # Add more transactions as needed...
]


# Function to get access token
def get_access_token(client_id, client_secret, token_url):
    response = requests.post(
        token_url,
        auth=HTTPBasicAuth(client_id, client_secret),
        data={
            'grant_type': 'client_credentials',
            'scope': 'all'
        }
    )

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")


# Function to get average footprints
def get_average_footprint(access_token, account_id):
    avg_footprints_url = 'https://api.staging.ecolytiq.arm.ecolytiq.network/footprints/v1/averages'
    params = {
        'account_id': account_id
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(
        avg_footprints_url,
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        result = response.json()
        average_footprint = result.get('footprint')
        return average_footprint
    else:
        raise Exception(f"Failed to get average footprint: {response.text}")


# Function to get footprints by category
def get_footprints_by_category(access_token, account_id, month, transactions):
    footprints_url = 'https://api.sandbox.arm.ecolytiq.network/statistic/v1/footprints/averages'
    params = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Prepare payload from transactions
    payload = {
        "transactions": transactions
    }

    response = requests.post(
        footprints_url,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get footprints by category: {response.text}")


##############################

try:
    access_token = get_access_token(client_id, client_secret, token_url)
    print("Access Token:", access_token)

    account_id = '5a73582adf954cf6b3db6cc97bedccd9'
    month = '2023-05'

    # Fetch average footprint
    average_footprint = get_average_footprint(access_token, account_id)
    print("Average Footprint:", average_footprint)

    # Optionally, fetch footprints by category using transactions
    footprints_by_category = get_footprints_by_category(access_token, account_id, month, transactions)
    print("Footprints by Category:", footprints_by_category)

except Exception as e:
    print(str(e))
