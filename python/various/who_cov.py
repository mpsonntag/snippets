import json
import os
import requests

w_dir = os.path.join(os.environ.get("HOME"), "Chaos", "DL")

furl = "https://covid19.who.int/page-data/region/euro/country/at/page-data.json"

res = requests.get(furl)

data = json.loads(res.text)

print(data["result"]["pageContext"]["countryCode"])


