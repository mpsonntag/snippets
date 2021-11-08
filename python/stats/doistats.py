import requests

DOI_MAIN_URL = "https://doi.gin.g-node.org/index.html"


def main():
    content = requests.get(DOI_MAIN_URL)
    contlist = content.text.splitlines()
    dates_list = []
    for line in contlist:
        if "<td>" in line and "-" in line and not "<a" in line:
            dates_list.append(line.strip().replace("<td>", "").replace("</td>", ""))
    print(dates_list)


if __name__ == "__main__":
    main()
