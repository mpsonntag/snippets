import lxml.etree as ET


def odml_to_html(odml_filename):
    # loading an odML xml file containing a full and valid stylesheet tag
    dom = ET.parse(odml_filename)
    style = dom.xpath("/odML")
    if not style:
        print("Could not find odML tag")
        return
    getstyle = style[0].findall("{http://www.w3.org/1999/XSL/Transform}stylesheet")
    if not getstyle:
        print("Could not find custom stylesheet tag")
        return
    transform = ET.XSLT(getstyle[0])
    newdom = transform(dom)
    html = ET.tostring(newdom, pretty_print=True).decode()

    outfile = "output.html"
    with open(outfile, "w") as fip:
        fip.write(html)


odml_to_html("resources/browser_display/custom_style.odml")
