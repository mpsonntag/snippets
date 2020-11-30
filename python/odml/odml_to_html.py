import lxml.etree as ET


def disp_html(xml_filename, xsl_filename):
    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    print(ET.tostring(newdom, pretty_print=True))


def display_odML_as_html(odML_file, xsl_file='odml.xsl'):
    # generate html representation from odML file and style sheet
    dom = ET.parse(odML_file)
    xslt = ET.parse(xsl_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)    # display html
    # display(HTML(ET.tostring(newdom, pretty_print=True).decode()))
