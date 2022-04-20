import requests
import os
from decouple import config

# Load env Vars
TOKEN = os.getenv("PURGE_TOKEN", None)
if not TOKEN:
    TOKEN = config("PURGE_TOKEN")

IDENTIFIER = os.getenv("PURGE_IDENTIFIER", None)
if not IDENTIFIER:
    IDENTIFIER = config("PURGE_IDENTIFIER")

# Prepare
headers = {
    "Authorization": "Bearer %s" % TOKEN,
    'Content-Type': 'application/json',
}

data = {
    'purge_everything': True
}

# Send requests
r = requests.post('https://api.cloudflare.com/client/v4/zones/%s/purge_cache' % IDENTIFIER, json = data, headers=headers)

# Show result
result = r.json()

print("success: %s" % result['success'])
print("errors: %s" % result['errors'])
print("messages: %s" % result['messages'])