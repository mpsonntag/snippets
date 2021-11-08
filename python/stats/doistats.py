import requests

DOI_MAIN_URL = "https://doi.gin.g-node.org/index.html"


def main():
    content = requests.get(DOI_MAIN_URL)
    print(content.text)


if __name__ == "__main__":
    main()
