------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

RDFReader write function

    def write_file(self, filename, doc_format, output_path):
        """
        Writes result to specified output_path if rdf doc contains exactly one odml document.
        If several odml docs found - creates files in specified directory and writes parsed docs to them.
        Example of created file: /<dir_path>/doc_<id>.odml (<id> - id of the document).

        :param filename: path to input file
        :param doc_format: rdf format of the file
        :param output_path: path to the output file or directory
        """
        self.g = Graph().parse(source=filename, format=doc_format)
        self.to_odml()
        if len(self.docs) > 1 and os.path.isdir(output_path):
            if os.path.exists(output_path):
                for doc in self.docs:
                    if doc:
                        path = os.path.join(output_path, "doc_" + doc.id)
                        odml.save(doc, path)
        elif len(self.docs) > 1 and not os.path.isdir(output_path):
            raise ValueError("Input file consists of multiple odml docs. output_path is not a valid path to directory.")
        elif len(self.docs) == 1 and os.path.isfile(output_path):
            odml.save(self.docs[0], output_path)
        elif len(self.docs) == 1 and not os.path.isfile(output_path):
            raise ValueError("Input file consists of a one odml doc. "
                             "output_path is not a valid path to the output file.")

-----------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

python-odml: odml.tools.xmlparser - fix parsing value.unit and type from v1.0

    # Quick fix to allow export of type and units from odml v1.0 values.
    # Does not account for differing units and dtypes within a single property.
    if tag == "value":
        for vn in node:
            if vn.tag == "type" and vn.text:
                arguments["dtype"] = vn.text
            elif vn.tag == "unit" and vn.text:
                arguments["unit"] = vn.text

    # Special handling of values
    if tag == "value" and node.text:
        content = from_csv(node.text.strip())
        arguments[tag] = content
    else:
        arguments[tag] = node.text.strip(
        ) if node.text else None

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

python-odml: multiple places where valid arguments are checked.

            self.is_valid_argument(node.tag, fmt, root, node)
            if node.tag in fmt._args:

            def is_valid_argument(self, tag_name, ArgClass, parent_node, child=None):
            if tag_name not in ArgClass._args:
