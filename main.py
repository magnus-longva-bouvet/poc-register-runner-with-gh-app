#!/usr/bin/env python3
import jwt
import time
import sys
import requests

# Get PEM file path
pem = "/home/magnus/.ssh/runner-token-generator.2023-11-21.private-key.pem" #debug
app_id = "640983" #debug


# if len(sys.argv) > 1:
#     pem = sys.argv[1]
# else:
#     pem = input("Enter path of private PEM file: ")
#
# # Get the App ID
# if len(sys.argv) > 2:
#     app_id = sys.argv[2]
# else:
#     app_id = input("Enter your APP ID: ")

# Open PEM
with open(pem, 'rb') as pem_file:
    signing_key = jwt.jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': app_id
}

# Create JWT
jwt_instance = jwt.JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')
headers={"Authorization": f"Bearer {encoded_jwt}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

res = requests.get("https://api.github.com/app/installations", headers=headers)
print(f"retrieving app installations endpoint: {res.status_code}")
res_json = res.json()
installation_id = res_json[0]['id']

res = requests.post(f"https://api.github.com/app/installations/{installation_id}/access_tokens", headers=headers)
new_token = res.json()['token']

headers["Authorization"] = f"Bearer {new_token}"

res = requests.get("https://api.github.com/orgs/magnublo-test-organization", headers=headers)
print(f"retrieving org metadata: {res.status_code}")
#print(res.json()['message'])
res = requests.post("https://api.github.com/orgs/magnublo-test-organization/actions/runners/registration-token", headers=headers)
print(f"retrieving registration token endpoint: {res.status_code}")
print(res.json()['token'])
#print(res.json()['message'])