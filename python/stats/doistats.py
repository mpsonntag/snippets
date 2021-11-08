import requests

import matplotlib.pyplot as plt

DOI_MAIN_URL = "https://doi.gin.g-node.org/index.html"


def plot_month(dates_list):
    """
    Parse the month from a list of YYYY-MM-DD formatted
    dates and plot them.
    :param dates_list:list of YYYY-MM-DD formatted dates
    """
    month_label = []
    month_sum = []
    curr_month = 0
    curr_sum = 0
    for entry in dates_list:
        check = f"%s-%s" % (entry.split("-")[0], entry.split("-")[1])
        if check != curr_month:
            if curr_month != 0:
                month_label.append(check)
                month_sum.append(curr_sum)
            curr_month = check
            curr_sum = 0
        curr_sum += 1

    # include latest month
    month_label.append(str(curr_month))
    month_sum.append(curr_sum)

    plt.plot(month_label, month_sum, label="Plot DOI publication months")
    plt.xticks(rotation=90)
    plt.xlabel("Months")
    plt.ylabel("Publications per month")
    plt.show()


def main():
    content = requests.get(DOI_MAIN_URL)
    contlist = content.text.splitlines()
    dates_list = []
    for line in contlist:
        if "<td>" in line and "-" in line and not "<a" in line:
            dates_list.append(line.strip().replace("<td>", "").replace("</td>", ""))

    plot_month(dates_list)


if __name__ == "__main__":
    main()
