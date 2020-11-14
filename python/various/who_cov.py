import copy
import json

from datetime import datetime
from os import environ, path

import numpy as np
import requests

from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
from pandas import DataFrame as PanDataFrame

OUT_DIR = path.join(environ.get("HOME"), "Chaos", "DL")
OUT_FILE_NAME = "cov19"

EURO_MAPPING = {"at": "Austria", "be": "Belgium", "ba": "Bosnia and Herzegovina", "bg": "Bulgaria",
                "hr": "Croatia", "cy": "Cyprus", "cz": "Czechia", "dk": "Denmark", "ee": "Estonia",
                "fi": "Finland", "fr": "France", "de": "Germany", "gr": "Greece", "hu": "Hungary",
                "ie": "Ireland", "it": "Italy", "lv": "Latvia", "li": "Liechtenstein",
                "lt": "Lithuania", "lu": "Luxembourg", "nl": "Netherlands", "no": "Norway",
                "pl": "Poland", "pt": "Portugal", "ro": "Romania", "rs": "Serbia", "sk": "Slovakia",
                "si": "Slovenia", "es": "Spain", "se": "Sweden", "ch": "Switzerland",
                "gb": "United Kingdom"}

REGIONS = {"amro": ["us"],
           "euro": EURO_MAPPING.keys()}

POPULATION = {"at": 8901000, "be": 11431000, "ba": 3531000, "bg": 6951000,
              "hr": 4190000, "cy": 1189000, "cz": 10637000, "dk": 5822000, "ee": 1323000,
              "fi": 5517000, "fr": 66993000, "de": 83166000, "gr": 10277000, "hu": 9773000,
              "ie": 4761000, "it": 60260000, "lv": 1934000, "li": 38000,
              "lt": 2794000, "lu": 626000, "nl": 17290000, "no": 5367000,
              "pl": 38386000, "pt": 10600000, "ro": 20121000, "rs": 7057000, "sk": 5450000,
              "si": 2064000, "es": 47100000, "se": 10327000, "ch": 8601000,
              "gb": 66435000, "us": 328000000}

# New data structure
CASES_DAY_DESCRIPTION = {"key": ["unix_timestamp"],
                         "values": ["cases_per_day_confirmed", "cases_cumulative",
                                    "cases_cumulative_percent_population",
                                    "deaths_per_day_confirmed", "deaths_cumulative",
                                    "deaths_cumulative_permil_population"]}
full_data = {"cases_per_day_data_description": CASES_DAY_DESCRIPTION,
             "countries": {}}


def fetch_data(full_data):
    # data dimensions; (1) timestamp, (2), region, (3) deaths, (4) cumulative deaths,
    # (5) deaths last 7 days, (6) Deaths Last 7 Days Change, (7) Deaths Per Million, (8) Confirmed,
    # (9) Cumulative confirmed, (10) Cases Last 7 Days, (11) Cases Last 7 Days Change,
    # (12) Cases Per Million
    furl = "https://covid19.who.int/page-data/region/%s/country/%s/page-data.json"

    # Fetch and convert data from all regions of interest
    for reg in REGIONS:
        for country_id in REGIONS[reg]:
            country_name = "United States"
            region = "america"
            if country_id != "us":
                country_name = EURO_MAPPING[country_id]
                region = "euro"

            curr_url = furl % (reg, country_id)
            res = requests.get(curr_url)
            print("Fetching country: '%s/%s' at \n\t%s" % (country_id, country_name, curr_url))
            data = json.loads(res.text)

            # Reduce to "timestamp: [confirmed, confirmed_cumulative,
            #                        case_cumulative_percent_population,
            #                        deaths, deaths_cumulative, death_cumulative_permil_population]"
            curr_country = {}
            curr_data = data["result"]["pageContext"]["countryGroup"]["data"]["rows"]
            curr_perc_pop = POPULATION[country_id] / 100
            curr_perm_pop = POPULATION[country_id] / 1000
            for i in curr_data:
                case_perc_pop = round(i[8]/curr_perc_pop, 3)
                death_perm_pop = round(i[3]/curr_perm_pop, 3)

                curr_country[i[0]] = [i[7], i[8], case_perc_pop, i[2], i[3], death_perm_pop]

            print("\tLatest cases: %s" % curr_country[list(curr_country.keys())[-1]])
            full_data["countries"][country_id] = {"country_name": country_name,
                                                  "region": region,
                                                  "population": POPULATION[country_id],
                                                  "cases": curr_country}

    return full_data


def save_to_json(data):
    # Save data structure to json file
    fn = path.join(OUT_DIR, ("%s.json" % OUT_FILE_NAME))
    print("\nWriting to file %s" % fn)
    with open(fn, "w") as fp:
        json.dump(data, fp)


def congregate_euro_cases(data):
    # congregate data; get euro sum
    euro_cases = {"country_name": "EU",
                  "population": 0,
                  "cases_total": [],
                  "cases": {}}

    for i in data["countries"]:
        if i != "us":
            euro_cases["population"] = euro_cases["population"] + \
                                       data["countries"][i]["population"]
            curr_cases = copy.deepcopy(data["countries"][i]["cases"])

            # Congregate latest total euro cases
            if not euro_cases["cases_total"]:
                euro_cases["cases_total"] = curr_cases[list(curr_cases.keys())[-1]]
            else:
                curr_list = curr_cases[list(curr_cases.keys())[-1]]
                euro_cases["cases_total"] = [sum(x) for x in
                                             zip(euro_cases["cases_total"], curr_list)]

            # Congregate daily total euro cases
            if not euro_cases["cases"]:
                euro_cases["cases"] = curr_cases
            else:
                for j in curr_cases:
                    euro_cases["cases"][j] = [sum(x) for x in
                                              zip(euro_cases["cases"][j], curr_cases[j])]

    # Fix euro percentages
    curr_perc_pop = euro_cases["population"] / 100
    curr_perm_pop = euro_cases["population"] / 1000

    # Euro percentage cases total
    euro_cases["cases_total"][2] = round(euro_cases["cases_total"][1] / curr_perc_pop, 3)
    euro_cases["cases_total"][5] = round(euro_cases["cases_total"][4] / curr_perm_pop, 3)

    # Euro percentages per day
    for i in euro_cases["cases"]:
        euro_cases["cases"][i][2] = round(euro_cases["cases"][i][1] / curr_perc_pop, 3)
        euro_cases["cases"][i][5] = round(euro_cases["cases"][i][4] / curr_perm_pop, 3)

    return euro_cases


def basic_data(euro_data, us_data):
    # Basic plots - prepare data
    cases_dates = []
    confirmed = []
    confirmed_cumulative = []
    case_cumulative_percent_population = []
    deaths = []
    deaths_cumulative = []
    death_cumulative_permil_population = []

    for i in euro_data["cases"]:
        cases_dates.append(datetime.fromtimestamp(i/1000))
        confirmed.append(euro_data["cases"][i][0])
        confirmed_cumulative.append(euro_data["cases"][i][1])
        case_cumulative_percent_population.append(euro_data["cases"][i][2])
        deaths.append(euro_data["cases"][i][3])
        deaths_cumulative.append(euro_data["cases"][i][4])
        death_cumulative_permil_population.append(euro_data["cases"][i][5])

    # dirty fix to compare euro to us (us sometimes is a day ahead in terms of numbers.)
    last_euro_date = cases_dates[-1]

    usconfirmed = []
    usconfirmed_cumulative = []
    uscase_cumulative_percent_population = []
    usdeaths = []
    usdeaths_cumulative = []
    usdeath_cumulative_permil_population = []

    for i in us_data:
        usconfirmed.append(us_data[i][0])
        usconfirmed_cumulative.append(us_data[i][1])
        uscase_cumulative_percent_population.append(us_data[i][2])
        usdeaths.append(us_data[i][3])
        usdeaths_cumulative.append(us_data[i][4])
        usdeath_cumulative_permil_population.append(us_data[i][5])
        if last_euro_date == datetime.fromtimestamp(i/1000):
            break

    return cases_dates, confirmed, usconfirmed


def plot_euro_us_comparison(dates, euro_confirmed, us_confirmed):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(dates, euro_confirmed, label="European zone")
    ax.plot(dates, us_confirmed, label="United States")
    ax.set_title("Per day Covid19 cases")
    ax.set_xlabel("Date")
    ax.legend(loc='upper left', fontsize='xx-small')
    plt.show()


def plot_all_country_cases(data, cases_dates):
    fig2 = plt.figure()
    ax = plt.subplot(111)

    markers_available = list(Line2D.markers.keys())
    marker_idx = -1
    for j in full_data["countries"]:
        if full_data["countries"][j]["region"] == "america":
            continue

        country = data["countries"][j]["country_name"]
        print("Working on %s" % country)

        curr_confirmed = []
        curr_data = data["countries"][j]["cases"]
        for i in curr_data:
            curr_confirmed.append(curr_data[i][0])

        # Handle individual markers
        marker_idx = marker_idx + 1
        ax.plot(cases_dates, curr_confirmed, label=country, marker=markers_available[marker_idx])

    ax.set_title("Per day cases euro countries")
    ax.set_xlabel("Date")
    ax.legend(loc='upper left', fontsize='xx-small')
    plt.show()


def plot_all_countries_last_month(full_data, cases_dates):
    # plot last 30 days euro zone
    fig3 = plt.figure()
    ax = plt.subplot(111)

    curr_len = len(cases_dates)
    markers_available = list(Line2D.markers.keys())
    marker_idx = -1
    for j in full_data["countries"]:
        if full_data["countries"][j]["region"] == "america":
            continue

        country = full_data["countries"][j]["country_name"]
        print("Working on %s" % country)

        curr_confirmed = []
        curr_data = full_data["countries"][j]["cases"]
        for i in curr_data:
            curr_confirmed.append(curr_data[i][0])

        # Handle individual markers
        marker_idx = marker_idx + 1
        ax.plot(cases_dates[curr_len-30:curr_len-1], curr_confirmed[curr_len-30:curr_len-1],
                label=country, marker=markers_available[marker_idx])

    ax.set_title("Per day cases euro countries; last 30 days")
    ax.set_xlabel("Date")
    ax.legend(loc='upper left', fontsize='xx-small')
    plt.show()


def get_aggregated(use_date, curr_cases, euro_cases):
    euro_stat = euro_cases["cases"][use_date]
    us_stat = curr_cases["us"]["cases"][use_date]
    names = ["Europe", "United states"]

    aggregated = list()
    aggregated.append(euro_stat)
    aggregated.append(us_stat)

    for i in curr_cases:
        if curr_cases[i]["region"] == "america":
            continue
        country = curr_cases[i]["country_name"]
        print("Working on %s" % country)

        names.append(country)
        aggregated.append(curr_cases[i]["cases"][use_date])

    return names, aggregated


def plot_cases_bar(euro_stat, labels, use_date):
    # bar plot statistics current state
    x = np.arange(len(labels))
    curr_date_string = datetime.fromtimestamp(use_date/1000)
    plt.title = "Cases overview (%s)" % curr_date_string
    plt.bar(x, euro_stat)
    plt.show()


def plot_table_country_statistics(row_labels, column_labels, aggregated):
    # Format large numbers with comma as 1000 separator
    format_aggregated = copy.deepcopy(aggregated)
    for line_idx, _ in enumerate(format_aggregated):
        for val_idx, val in enumerate(format_aggregated[line_idx]):
            format_aggregated[line_idx][val_idx] = f'{val:,}'

    _, ax = plt.subplots()

    # Hide axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # Hide figure border
    for spine_location in ax.spines:
        ax.spines[spine_location].set_visible(False)

    tbl = ax.table(cellText=format_aggregated, rowLabels=row_labels,
                   colLabels=column_labels, loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(range(len(column_labels)))

    plt.tight_layout()
    plt.show()


def formatted_statistics(full_data, euro_cases):
    # different stats
    sum_only = list()
    use_date = list(euro_cases["cases"].keys())[-1]
    sum_only_cases = copy.deepcopy(full_data["countries"])

    # format large numbers with comma as 1000 separator
    curr_stat = copy.deepcopy(euro_cases["cases"][use_date])
    curr_pop = f'{copy.deepcopy(euro_cases["population"]):,}'
    curr_case_sum = f'{curr_stat[1]:,}'
    curr_case_per = f'{curr_stat[2]:,}'
    curr_death_sum = f'{curr_stat[4]:,}'
    curr_death_per = f'{curr_stat[5]:,}'
    sum_only.append([curr_pop, curr_case_sum, curr_case_per, curr_death_sum, curr_death_per])

    curr_stat = sum_only_cases["us"]["cases"][use_date]
    curr_pop = f'{sum_only_cases["us"]["population"]:,}'
    curr_case_sum = f'{curr_stat[1]:,}'
    curr_case_per = f'{curr_stat[2]:,}'
    curr_death_sum = f'{curr_stat[4]:,}'
    curr_death_per = f'{curr_stat[5]:,}'
    sum_only.append([curr_pop, curr_case_sum, curr_case_per, curr_death_sum, curr_death_per])

    names = ["Europe", "United states"]

    for i in sum_only_cases:
        if sum_only_cases[i]["region"] == "america":
            continue

        country = sum_only_cases[i]["country_name"]
        print("Working on %s" % country)

        curr_stat = sum_only_cases[i]["cases"][use_date]
        curr_pop = f'{sum_only_cases[i]["population"]:,}'
        curr_case_sum = f'{curr_stat[1]:,}'
        curr_case_per = f'{curr_stat[2]:,}'
        curr_death_sum = f'{curr_stat[4]:,}'
        curr_death_per = f'{curr_stat[5]:,}'
        sum_only.append([curr_pop, curr_case_sum, curr_case_per, curr_death_sum, curr_death_per])

        names.append(country)

    return sum_only, names


def plot_table_formatted_country_statistics(sum_only, row_labels, column_labels):
    _, ax = plt.subplots()

    # Hide axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # Hide figure border
    for spine_location in ax.spines:
        ax.spines[spine_location].set_visible(False)

    tbl = ax.table(cellText=sum_only, rowLabels=row_labels,
                   colLabels=column_labels, loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(range(len(column_labels)))

    plt.tight_layout()
    plt.show()


def pandas_formatted_country_statistics(sum_only, names, col_labels):
    # Using pandas to print table sorted by perc population descending
    d_sum_only = {}

    idx = 0
    for curr_list in sum_only:
        d_sum_only[names[idx]] = curr_list
        idx = idx + 1

    sum_frame = PanDataFrame(d_sum_only, col_labels)

    sort_by = "[%] population"
    # sort_by = "[‰] population"
    print(sum_frame.transpose().sort_values(by=[sort_by], ascending=False))


def formatted_statistics_last_week(full_data):
    # calc sum infections last seven days
    days = list(full_data["countries"]["at"]["cases"].keys())[-8:-1]

    curr_data = {}
    curr_plot = {}
    for ccode in full_data["countries"]:
        access_data = full_data["countries"][ccode]
        curr_cases = {}

        sum_cases = 0
        for i in days:
            curr_cases[i] = access_data["cases"][i]
            sum_cases = sum_cases + access_data["cases"][i][0]

        perc_cases = round(sum_cases / (access_data["population"]/100), 3)
        curr_data[ccode] = {"country_name": access_data["country_name"],
                            "population": f'{access_data["population"]:,}',
                            "sum_cases": f'{sum_cases:,}',
                            "perc_cases": perc_cases,
                            "cases": copy.deepcopy(curr_cases)
                           }
        curr_plot[access_data["country_name"]] = [f'{access_data["population"]:,}',
                                                  f'{sum_cases:,}',
                                                  perc_cases]

    return curr_plot


def pandas_country_last_week(curr_plot):
    # Add seven days info table
    day_col_labels = ["population", "cases last 7 days", "[%] population"]

    sum_frame = PanDataFrame(curr_plot, day_col_labels)
    print(sum_frame.transpose().sort_values(by=["[%] population"], ascending=False))


def plot_percent_countries(full_data, cases_dates):
    # per day percent plot to properly compare increase rates per citizen
    ax = plt.subplot(111)

    markers_available = list(Line2D.markers.keys())
    marker_idx = -1
    for j in full_data["countries"]:
        if full_data["countries"][j]["region"] == "america":
            continue

        country = full_data["countries"][j]["country_name"]
        # print("Working on %s" % country)

        population = full_data["countries"][j]["population"]
        curr_per_day_perc = []
        curr_data = full_data["countries"][j]["cases"]
        for i in curr_data:
            curr_val = round(curr_data[i][0] / (population / 1000), 3)
            curr_per_day_perc.append(curr_val)

        # Handle individual markers
        marker_idx = marker_idx + 1
        ax.plot(cases_dates, curr_per_day_perc, label=country, marker=markers_available[marker_idx])

    ax.set_title("Per day % population increase euro countries")
    ax.set_xlabel("Date")
    ax.legend(loc='upper left', fontsize='xx-small')
    plt.show()


full_data = fetch_data(full_data)
save_to_json(full_data)

euro_cases = congregate_euro_cases(full_data)
us_cases = full_data["countries"]["us"]["cases"]
cases_dates, confirmed, usconfirmed = basic_data(euro_cases, us_cases)

# change default figure size
rcParams['figure.figsize'] = (8.5, 4.4)
plot_euro_us_comparison(cases_dates, confirmed, usconfirmed)
plot_all_country_cases(full_data, cases_dates)
plot_all_countries_last_month(full_data, cases_dates)

# display current numpy print options
print(np.get_printoptions())
# set precision to 3
np.set_printoptions(precision=3)

use_date = list(euro_cases["cases"].keys())[-1]
curr_cases = copy.deepcopy(full_data["countries"])
names, aggregated = get_aggregated(use_date, curr_cases, euro_cases)

labels = ["cases", "cumulative", "[%] population", "deaths", "cumulative", "[‰] population"]
# plot_table_country_statistics(names, labels, aggregated)

sum_only, names = formatted_statistics(full_data, euro_cases)

col_labels = ["population", "sum_cases", "[%] population", "sum_deaths", "[‰] population"]
# plot_table_formatted_country_statistics(sum_only, names, col_labels)
pandas_formatted_country_statistics(sum_only, names, col_labels)

curr_plot = formatted_statistics_last_week(full_data)

pandas_country_last_week(curr_plot)

plot_percent_countries(full_data, cases_dates)
