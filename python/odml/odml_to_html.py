"""
Load an odML xml file containing a full and valid stylesheet tag and
use the stylesheet information to transform the odml document to html.
"""
import argparse

from lxml import etree


LOCAL_FILE = "resources/browser_display/custom_style.odml"


def odml_to_html(odml_filename):
    """
    Load an odML xml file containing a full and valid stylesheet tag and
    use the stylesheet information to transform the odml document to html.

    :param odml_filename: odML XML file containing a full custom XSLT style.
    """
    dom = etree.parse(odml_filename)
    style = dom.xpath("/odML")
    if not style:
        print("Could not find odML tag")
        return
    getstyle = style[0].findall("{http://www.w3.org/1999/XSL/Transform}stylesheet")
    if not getstyle:
        print("Could not find custom stylesheet tag")
        return
    transform = etree.XSLT(getstyle[0])
    newdom = transform(dom)
    html = etree.tostring(newdom, pretty_print=True).decode()

    outfile = "output.html"
    with open(outfile, "w", encoding="utf-8") as fip:
        fip.write(html)


def run():
    """
    Handle command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("odml_file", help="odml file containing custom stylesheet")
    args = parser.parse_args()

    odml_file = args.odml_file
    odml_to_html(odml_file)


if __name__ == "__main__":
    run()
