"""
Fetch DOI publication page and parse dates from table entries.
"""
import calendar
import requests

import matplotlib.pyplot as plt

DOI_MAIN_URL = "https://doi.gin.g-node.org/index.html"


def plot_month(dates_list):
    """
    Parse the month from a list of YYYY-MM-DD formatted
    dates and plot them.
    :param dates_list:list of YYYY-MM-DD formatted dates
    """
    dates_list = list(reversed(dates_list))

    timeline = {}
    abs_sum = {}
    for entry in dates_list:
        check = f"{entry.split('-')[0]}-{entry.split('-')[1]}"
        if check not in timeline:
            timeline[check] = 0
        timeline[check] = timeline[check] + 1

        mon = int(entry.split("-")[1])
        if mon not in abs_sum:
            abs_sum[mon] = 0
        abs_sum[mon] = abs_sum[mon] + 1

    # plot publication timeline
    plt.bar(list(timeline.keys()), list(timeline.values()),
            label="Plot DOI publication timeline")
    plt.xticks(rotation=75)
    plt.xlabel("Months")
    plt.ylabel("Publications per month")
    plt.show()

    # month numbers to month names
    sorted_months = []
    for mon in sorted(abs_sum):
        sorted_months.append(calendar.month_name[mon])

    x_data = sorted_months
    y_data = []
    for key in sorted(abs_sum):
        y_data.append(abs_sum[key])

    # plot absolute numbers per month
    plt.bar(x_data, y_data, label="Plot DOI publications / months")
    plt.xticks(rotation=75)
    plt.xlabel("Months")
    plt.ylabel("Publications per month")
    plt.show()


def fetch_dates_list():
    """
    Fetch DOI publication page and parse dates from table entries.
    :return: list of YYYY-MM-DD formatted dates
    """
    content = requests.get(DOI_MAIN_URL)
    dates_list = []
    for line in content.text.splitlines():
        if "<td>" in line and "-" in line and "<a" not in line:
            dates_list.append(line.strip().replace("<td>", "").replace("</td>", ""))
    return dates_list


def main():
    """
    Fetch DOI publication dates and plot statistics
    """
    dates_list = fetch_dates_list()

    plot_month(dates_list)


if __name__ == "__main__":
    main()
