from api import unifi
import requests

STUDENT_COUNT = 30

response = requests.get(f"https://randomuser.me/api/?results={STUDENT_COUNT}")
if response.status_code == 200:
    data = response.json()
    usernames = [user['login']['username'] for user in data['results']]
else:
    raise Exception("Failed to fetch usernames from the API")

for username in usernames:
    unifi.add_radius_user(username, "supersecurepassword")