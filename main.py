import requests
import json
import os
from dotenv import main as env
env.load_dotenv()

# Get the episodes to delete from the episodes_to_delete.json file.
EPISODE_HISTORY = json.loads(open("episodes_to_delete.json").read())["episodes"]
# Get the API URL from the .env file.
API_URL = str(os.getenv('API_URL'))
# Set the headers for the API requests.
HEADERS = {
    "Content-Type": "application/json",
    "trakt-api-version": "2",
    "trakt-api-key":  os.getenv('CLIENT_ID'),
    "Authorization": "Bearer ",
}

# Create a new authorization code with the client_id. https://trakt.docs.apiary.io/#reference/authentication-devices/device-code
request = requests.post(API_URL + str(os.getenv('CREATE_AUTH')), headers={"Content-Type": "application/json"}, data=json.dumps({"client_id": os.getenv('CLIENT_ID')}))
response = request.json()

print("Go to: " + response["verification_url"] + " and enter code: " + response["user_code"])
input("Press Enter to continue...")

# Get the authorization code with the client_id and client_secret. # https://trakt.docs.apiary.io/#reference/authentication-devices/get-token
request = requests.post(API_URL + str(os.getenv('GET_AUTH')), headers={"Content-Type": "application/json"}, data=json.dumps({"client_id": os.getenv('CLIENT_ID'), "client_secret": os.getenv('CLIENT_SECRET'), "code": response["device_code"]}))
response = request.json()

# Add the access token to the headers.
HEADERS["Authorization"] = HEADERS["Authorization"] + response["access_token"]

# Get episodes's watch history to delete.
while True:
    # Create a new dictionary to store the episodes to delete.
    EPISODES_TO_DELETE = {"ids": []}

    for episode in EPISODE_HISTORY:
        # Get the episodes's watch history. # https://trakt.docs.apiary.io/#reference/sync/get-history/remove-items-from-history
        request = requests.get(API_URL + str(os.getenv('EPISODE_HISTORY')) + str(episode["id"]), headers=HEADERS)
        response = request.json()

        # Check is episode play id is not in the blacklist. If not, add it to the episodes to delete.
        for item in response: 
            if item["id"] != episode["blacklist_id"]:
                EPISODES_TO_DELETE["ids"].append(item["id"])

    # Check if there are no episodes to delete. If not, break the loop.
    if len(EPISODES_TO_DELETE["ids"]) == 0: break
    print(EPISODES_TO_DELETE)

    # Remove episodes from the watch history. # https://trakt.docs.apiary.io/#reference/sync/get-history/remove-items-from-history
    request = requests.post(API_URL + str(os.getenv('REMOVE_EPISODE')), headers=HEADERS, data=json.dumps(EPISODES_TO_DELETE))
    response = request.json()

    # Print the response.
    print(json.dumps(response, indent=4))


print("All episodes have been removed.")
exit(0)