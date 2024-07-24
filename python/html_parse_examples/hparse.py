import requests

from html.parser import HTMLParser


class CleanupHTMLParser(HTMLParser):
    def __init__(self):
        self.print_tag = ""
        super().__init__()

    @property
    def print_tag(self):
        return self._print_tag

    @print_tag.setter
    def print_tag(self, value):
        self._print_tag = value

    def handle_starttag(self, tag, attrs):
        if tag == "div" and "class" in attrs[0] and (
                "text-paragraph" in attrs[0][1] or "headerComp-intro" in attrs[0][1]):
            self.print_tag = " "

    def handle_data(self, data):
        pdat = data.strip()
        if self.print_tag and pdat:
            self.print_tag = f"{self.print_tag} {pdat}"

    def handle_endtag(self, tag):
        if tag == "div" and self.print_tag:
            print(self.print_tag.strip())
            self.print_tag = ""


def ref_par(get_url):
    get_req = requests.get(get_url)
    hpar = CleanupHTMLParser()
    hpar.feed(get_req.text)


fetch_url = 'https://kurier.at/chronik/welt/goebbels-villa-wandlitz-bogensee/402880892'

ref_par(fetch_url)
