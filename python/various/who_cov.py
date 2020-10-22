import json
import requests

from datetime import datetime
from matplotlib import pyplot as plt
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
        "hr": 4190000, "cy": 1189000, "cz": 10637000, "dk": 5822000, "ee": 1323000,
        "fi": 5517000, "fr": 66993000, "de": 83166000, "gr": 10277000, "hu": 9773000,
        "ie": 4761000, "it": 60260000, "lv": 1934000, "li": 38000,
        "lt": 2794000, "lu": 626000, "nl": 17290000, "no": 5367000,
        "pl": 38386000, "pt": 10600000, "ro": 20121000, "rs": 7057000, "sk": 5450000,
        "si": 2064000, "es": 47100000, "se": 10327000, "ch": 8601000,
        "gb": 66435000, "us": 328000000}

# New data structure
cases_day_description = {"key": ["unix_timestamp"],
                         "values": ["cases_per_day_confirmed", "cases_cumulative",
                                    "cases_cumulative_percent_population",
                                    "deaths_per_day_confirmed", "deaths_cumulative",
                                    "deaths_cumulative_permil_population"]}
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
        region = "euro"
        if country_id != "us":
            country_name = euro[country_id]
            region = "america"

        curr_url = furl % (reg, country_id)
        res = requests.get(curr_url)
        print("Fetching country: '%s/%s' at \n\t%s" % (country_id, country_name, curr_url))
        data = json.loads(res.text)

        # Reduce to "timestamp: [confirmed, confirmed_cumulative,
        #                        case_cumulative_percent_population,
        #                        deaths, deaths_cumulative, death_cumulative_permil_population]"
        curr_country = {}
        curr_data = data["result"]["pageContext"]["countryGroup"]["data"]["rows"]
        curr_perc_pop = population[country_id]/100
        curr_perm_pop = population[country_id]/1000
        for i in curr_data:
            case_perc_pop = round(i[8]/curr_perc_pop, 3)
            death_perm_pop = round(i[3]/curr_perm_pop, 3)

            curr_country[i[0]] = [i[7], i[8], case_perc_pop, i[2], i[3], death_perm_pop]

        full_data["countries"][country_id] = {"country_name": country_name,
                                              "region": region,
                                              "population": population[country_id],
                                              "cases": curr_country}

# Save data structure to json file
fn = path.join(out_dir, ("%s.json" % out_file_name))
print("\nWriting to file %s" % fn)
with open(fn, "w") as fp:
    json.dump(full_data, fp)

# congregate data; get euro sum

euro = {"country_name": "EU",
        "population": 0,
        "cases_total": [],
        "cases": {}}

for i in full_data["countries"]:
    if i != "us":
        euro["population"] = euro["population"] + full_data["countries"][i]["population"]
        curr_cases = full_data["countries"][i]["cases"]

        # Congregate latest total euro cases
        if not euro["cases_total"]:
            euro["cases_total"] = curr_cases[list(curr_cases.keys())[-1]]
        else:
            curr_list = curr_cases[list(curr_cases.keys())[-1]]
            euro["cases_total"] = [sum(x) for x in zip(euro["cases_total"], curr_list)]

        # Congregate daily total euro cases
        if not euro["cases"]:
            euro["cases"] = curr_cases
        else:
            for j in curr_cases:
                euro["cases"][j] = [sum(x) for x in zip(euro["cases"][j], curr_cases[j])]

# Fix euro percentages
curr_perc_pop = euro["population"]/100
curr_perm_pop = euro["population"]/1000

# Euro percentage cases total
euro["cases_total"][2] = round(euro["cases_total"][1]/curr_perc_pop, 3)
euro["cases_total"][5] = round(euro["cases_total"][4]/curr_perm_pop, 3)

# Euro percentages per day
for i in euro["cases"]:
    euro["cases"][i][2] = round(euro["cases"][i][1]/curr_perc_pop, 3)
    euro["cases"][i][5] = round(euro["cases"][i][4]/curr_perm_pop, 3)

# Basic plots - prepare data
# europe data as example

cases_dates = []
confirmed = []
confirmed_cumulative = []
case_cumulative_percent_population = []
deaths = []
deaths_cumulative = []
death_cumulative_permil_population = []

for i in euro["cases"]:
    cases_dates.append(datetime.fromtimestamp(i/1000))
    confirmed.append(euro["cases"][i][0])
    confirmed_cumulative.append(euro["cases"][i][1])
    case_cumulative_percent_population.append(euro["cases"][i][2])
    deaths.append(euro["cases"][i][3])
    death_cumulative_permil_population.append(euro["cases"][i][4])
    death_cumulative_permil_population.append(euro["cases"][i][5])

# dirty fix to compare euro to us (us sometimes is a day ahead in terms of numbers.)
last_euro_date = cases_dates[-1]

us_cases = full_data["countries"]["us"]["cases"]

uscases_dates = []
usconfirmed = []
usconfirmed_cumulative = []
uscase_cumulative_percent_population = []
usdeaths = []
usdeaths_cumulative = []
usdeath_cumulative_permil_population = []

for i in us_cases:
    usconfirmed.append(us_cases[i][0])
    usconfirmed_cumulative.append(us_cases[i][1])
    uscase_cumulative_percent_population.append(us_cases[i][2])
    usdeaths.append(us_cases[i][3])
    usdeath_cumulative_permil_population.append(us_cases[i][4])
    usdeath_cumulative_permil_population.append(us_cases[i][5])
    if last_euro_date == datetime.fromtimestamp(i/1000):
        break

title = "Per day Covid19 cases"
x_label = "Date"

plt.plot(cases_dates, confirmed, label="European zone")
plt.plot(cases_dates, usconfirmed, label="United States")
plt.title(title)
plt.xlabel(x_label)
plt.legend()
plt.show()
