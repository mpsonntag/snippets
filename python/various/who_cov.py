import json
import requests

from os import environ, path

out_dir = path.join(environ.get("HOME"), "Chaos", "DL")
out_file_name = "cov19"

euro = {"at": "Austria", "be": "Belgium", "ba": "Bosnia and Herzegovina", "bg": "Bulgaria",
        "hr": "Croatia", "cy": "Cyprus", "cz": "Czechia", "dk": "Denmark", "ee": "Estonia",
        "fi": "Finland", "fr": "France", "de": "Germany", "gr": "Greece", "hu": "Hungary",
        "ie": "Ireland", "it": "Italy", "lv": "Latvia", "li": "Liechtenstein",
        "lt": "Lithuania", "lu": "Luxembourg", "nl": "Netherlands", "no": "Norway",
        "pl": "Poland", "pt": "Portugal", "ro": "Romania", "rs": "Serbia", "sk": "Slovakia",
        "si": "Slovenia", "es": "Spain", "se": "Sweden", "ch": "Switzerland",
        "gb": "United Kingdom"}

regions = {"amro": ["us"],
           "euro": euro.keys()}

population = {"at": 8901000, "be": 11431000, "ba": 3531000, "bg": 6951000,
        "hr": 4190000, "cy": 1189265, "cz": 10637000, "dk": 5822000, "ee": 1323000,
        "fi": 5517000, "fr": 66993000, "de": 83166000, "gr": 10277000, "hu": 9773000,
        "ie": 4761000, "it": 60260000, "lv": 1934000, "li": 38000,
        "lt": 2794000, "lu": 626000, "nl": 17290000, "no": 5367000,
        "pl": 38386000, "pt": 10600000, "ro": 20121000, "rs": 7057000, "sk": 5450000,
        "si": 2064000, "es": 47100000, "se": 10327000, "ch": 8601000,
        "gb": 66435000, "us": 328000000}

# New data structure
cases_day_description = {"key": ["unix_timestamp"],
                         "values": ["cases_per_day_confirmed", "cases_cumulative",
                                    "deaths_per_day_confirmed", "deaths_cumulative"]}
full_data = {"cases_per_day_data_description": cases_day_description,
             "countries": {}}

# data dimensions; (1) timestamp, (2), region, (3) deaths, (4) cumulative deaths,
# (5) deaths last 7 days, (6) Deaths Last 7 Days Change, (7) Deaths Per Million, (8) Confirmed,
# (9) Cumulative confirmed, (10) Cases Last 7 Days, (11) Cases Last 7 Days Change,
# (12) Cases Per Million
furl = "https://covid19.who.int/page-data/region/%s/country/%s/page-data.json"

# Fetch and convert data from all regions of interest
for reg in regions:
    for country_id in regions[reg]:
        country_name = "United States"
        if country_id != "us":
            country_name = euro[country_id]

        curr_url = furl % (reg, country_id)
        res = requests.get(curr_url)
        print("Fetching country: '%s/%s' at \n\t%s" % (country_id, country_name, curr_url))
        data = json.loads(res.text)

        # Reduce to "timestamp: [confirmed, confirmed_cumulative, deaths, deaths_cumulative]"
        curr_country = {}
        curr_data = data["result"]["pageContext"]["countryGroup"]["data"]["rows"]
        for i in curr_data:
            curr_country[i[0]] = [i[7], i[8], i[2], i[3]]

        full_data["countries"][country_id] = {"country_name": country_name,
                                              "population": population[country_id],
                                              "cases": curr_country}

# Save data structure to json file
fn = path.join(out_dir, ("%s.json" % out_file_name))
print("\nWriting to file %s" % fn)
with open(fn, "w") as fp:
    json.dump(full_data, fp)
