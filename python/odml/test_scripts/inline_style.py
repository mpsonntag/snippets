import odml

doc = odml.Document()
sec = doc.create_section(name="secname")
prop = sec.create_property(name="propname", value=["a", "b", "c"])

template = """<xsl:template match="odML">
      <xsl:variable name="repository" select="repository"/>
      <html>
        <!-- <head> //-->
          <style type="text/css">
            Here style sheets
          </style>
        <!-- </head> //-->
        <body>
          Here HTML body
        </body>
      </html>
    </xsl:template>"""


file_default = "/home/msonntag/Chaos/DL/odml_style_default.xml"
file_style_odml = "/home/msonntag/Chaos/DL/odml_style_odml.xml"
file_style_custom = "/home/msonntag/Chaos/DL/odml_style_custom.xml"

odml.tools.XMLWriter(doc).write_file(file_default)
odml.tools.XMLWriter(doc).write_file(file_style_odml, local_style=True)
odml.tools.XMLWriter(doc).write_file(file_style_custom,
                                     local_style=True, custom_template=template)
