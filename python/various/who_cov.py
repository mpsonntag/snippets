import json
import os
import requests

euro = {"at": "Austria", "be": "Belgium", "ba": "Bosnia and Herzegovina", "bg": "Bulgaria",
        "hr": "Croatia", "cy": "Cyprus", "cz": "Czechia", "dk": "Denmark", "ee": "Estonia",
        "fi": "Finland", "fr": "France", "de": "Germany", "gr": "Greece", "hu": "Hungary",
        "ie": "Ireland", "it": "Italy", "lv": "Latvia", "li": "Liechtenstein",
        "lt": "Lithuania", "lu": "Luxembourg", "nl": "Netherlands", "no": "Norway",
        "po": "Poland", "pt": "Portugal", "ro": "Romania", "rs": "Serbia", "sk": "Slovakia",
        "si": "Slovenia", "es": "Spain", "se": "Sweden", "ch": "Switzerland",
        "gb": "United Kingdom"}

regions = {"amro": ["us"],
           "euro": euro.keys()}

w_dir = os.path.join(os.environ.get("HOME"), "Chaos", "DL")

furl = "https://covid19.who.int/page-data/region/%s/country/%s/page-data.json"

curr_url = furl % ("euro", "at")

res = requests.get(curr_url)
data = json.loads(res.text)

# data dimensions; (1) timestamp, (2), region, (3) deaths, (4) cumulative deaths,
# (5) deaths last 7 days, (6) Deaths Last 7 Days Change, (7) Deaths Per Million, (8) Confirmed,
# (9) Cumulative confirmed, (10) Cases Last 7 Days, (11) Cases Last 7 Days Change,
# (12) Cases Per Million

# Mangle to "timestamp: [confirmed, deaths]"
curr = {}
curr_data = data["result"]["pageContext"]["countryGroup"]["data"]["rows"]
for i in curr_data:
    curr[i[0]] = [i[7], i[2]]
