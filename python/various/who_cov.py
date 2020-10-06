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

furl = "https://covid19.who.int/page-data/region/euro/country/at/page-data.json"

res = requests.get(furl)

data = json.loads(res.text)

print(data["result"]["pageContext"]["countryCode"])


