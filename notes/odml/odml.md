------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

odml hierarchy example

Document
+-Section
| +-Property-[Values]
+-Section
  +-Section
  | +-Property-[Values]
  | +-Property-[Values]
  +-Section

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

------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------

odML library changes:

- unify import style

- when assigning the portal repository to a document, it cannot be properly loaded [xxx] (at least when setting repo and immediately displaying the document)

- main document: how is section.link actually supposed to work?

- refactor format:
    - make fields public
    - add model version here or in odml.__init__ -> there implementation specifics are already present.

- refactor xmlparser:
    - use format model version
    - add check for file version vs model version & print warning

- dumper:
    - move functionality to xmlparser

- refactor version_converter:
    - deal with filename: currently both class instantiation and convert_odml require an odml file
        -> should be either or?
    - remove write file method
    - use format model version
    - fix _fix_unmatching_tags

- odml: odml paper should be mentioned in tutorial and resources
- odml: resource cleanup after v1.4
- odml: remove http://www.g-node.org/projects/odml since it contains outdated information

- [lib|section] prohibit a section to have itself as a parent/child

- [lib|dtypes] does dtype "text" or "person" work?
- [lib|dtypes] extend and append for `tuple` fails
- [lib|dtypes] extend and append for `person` fails when using a string

- [lib|validation] Add validation help - ids for every specific message

- [lib|validation] Currently there is no re-validate whole document.
    - the current "validate" function should not be public
    - a new "validate" function should reset and rerun an existing validation.

- [lib/ui|validation] Obscure missing `Property.name` loading error
    - `name` is currently required for `Property` by the format.
    - If a property name is set to empty string and saved, the name tag will be set 
        to empty string, but will still be there. Therefore the validator will say: 
        Oh, name is here, thats nice, no reason to complain.
    - The file can be closed and saved, it will contain an empty name tag.
    - This file can be opened and the parser will say: Oh, name is here, that's how it should be.
    - But lo and behold, on the second save the name tag of the empty entity will be removed from
        the xml file and on load the xml parser will crash since the required property attribute
        is no longer there...
    - This should no longer be of an issue, since we are more lenient when loading xml
        odml files, but its still not very nicely handled.

- [lib|terminology] Small fixes
    - L11 ... never used
    - L62 ... use `with ... open` instead
    - L141: It seems that the file does not get closed properly.

- [lib|terminology] how is it currently ensured, that we always get the latest version
        from a server? is there a timestamp or a last changed date, that can be checked? 
        otherwise the local cache will never be updated, right?
        would be nicer to handle it via the last changed
        Mon, 20 Nov 2017 15:35:15 GMT
        could do a check for each file like here: https://stackoverflow.com/questions/9890815/python-get-headers-only-using-urllib2
        and use to compare with local file:
        
            last_mod = response.info().getheader('Last-Modified')

- [lib|terminologies] add check whether there is an internet connection and act appropriately if there is none.

- [lib|base.py] Connected to the issue terminology cache refresh issue: base.py deferred_load makes it hard to debug where a terminology is broken, because when one document is loaded, it immediately loads and parses all other documents that can be found via any <repository> tag, and since it is a deferred load, it's virtually impossible to find out which of the connected terminologies contains the error.
    plus: every time we even HOVER above any property in the ui, deferred_loading happens in the background, trying to load all connected terminologies.

- [lib|property.py] There is still an in-code import around L146 - issue

- [lib|sectionable] when merging sections, are subsections and properties checked whether name/type
    are still unique within the new section?

- [lib|xml/odmlparser] add test for parser ignore_error switch. (we have all the files for the failings)
- [lib|xmlparser] fix parsing value.unit and type from v1.0

    # Quick fix to allow export of type and units from odml v1.0 values.
    # Does not account for differing units and dtypes within a single property.
    if tag == "value":
        for vn in node:
            if vn.tag == "type" and vn.text:
                arguments["dtype"] = vn.text
            elif vn.tag == "unit" and vn.text:
                arguments["unit"] = vn.text

    # Special handling of values;
    curr_text = node.text.strip() if node.text else None
    if tag == "value" and curr_text:
       content = from_csv(curr_text)
        arguments[tag] = content
    else:
        arguments[tag] = curr_text

- [lib|xmlparser] add proper check and error message if file was not found when reading

- [lib] currently many checks for unique name; some checks for unique name/type; which should it be? 

- [lib|version_converter] Add log message test
- [lib|version_converter] Add _parse_document test
- [lib|version_converter] Add _handle_value test

- [lib|doc] doc.itervalues: in 1.4 returns just the values w/o any object information
    ... quite useless ...  should this be refactored to return all properties to emulate 
    the functionality from before where it returned the Value objects and therefore entry
    points into the odml tree from the value perspective? or remove and just use iterproperties.

- [lib|test] Random test_parser fails.
    When running the test often enough, one will encounter a random test fail with the following result:

        FAIL: test_yaml (test.test_parser.TestParser)
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/home/msonntag/Chaos/work/python-odml/test/test_parser.py", line 46, in test_yaml
            self.assertEqual(yaml_doc, self.odml_doc)
        AssertionError: <Doc 42 by D. N. Adams (2 sections)> != <Doc 42 by D. N. Adams (2 sections)>

    The next time tests are run, pass again. Also happens at line 64 sometimes.

- [lib|tests] `python -m unittest discover test` leads to failing tests with py2, 
        but not with `python setup.py test`.

- [lib|RDF] does the conversion of date/datetime/time work for RDF

- [lib|resources] Can we remove resources/install_osx...? I think the code has been moved to travis.yaml

- [lib|tools] provide an "isodmlfile" check for files.

