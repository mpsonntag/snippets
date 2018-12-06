------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

color palettes and pickers:

http://colorsafe.co/
http://colorpalettes.net/
https://htmlcolorcodes.com/color-picker/

odmltables color palette:

http://colorpalettes.net/color-palette-3599/
#34340d
#768a3a
#977528
#e5d2ab
#cfd3c3

---------
http://colorpalettes.net/color-palette-3477/

#83512e
#8b7717
#a49773
#ceccac
#e6e8d1

---------
http://colorpalettes.net/color-palette-3484/
http://colorpalettes.net/color-palette-2731/
#abad3d
#a4b650

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Issues

- [odml-tables & -ui] problems:
    - uses odml.format version 1.0 -> would require a transformation from 1.1 -> 1.0 if we use it from
        odml-ui v1.4 -> or we add a transformation to format 1.1 in odml-tables. -> which would mean 
        we would first need to get to a consensus whether and when Jülich 
        will switch to format version 1.1/odml version 1.4.
    - odml-tables only accepts xml files with the file ending `.odml`, we also use `.xml`.

- [odml-tables] when comparing more than 240 columns (why ever someone would want to do this), the following error occurs:

        An error occurred. This is the full error report:
        ValueError: column index (256) not an int in range(256)
        odmltables/gui/compsectionpages.py", line 408, in handlebuttonbrowse
        odmltables/gui/compsectionpages.py", line 446, in compare
        odmltables/gui/compsectionpages.py", line 429, in _saveXlsTable
        odmltables/compare_section_xls_table.py", line 99, in write2file

[tables] PyPI release plan?
[tables] what about unsupported odml tags?
[tables|1.4] _merge_odml_values in odml_table needs to be rewritten.

[tables] Check examples folder, which code needs to be updated to odML format version 1.4 as well.

[tables|version] use v1.0.0 for odml-core v1.4; use v0.2.0 for odml-core 1.3

[tables|version] make v0.2.0 PyPI release with Python2 and 3 fixes 

[tables|version] Version number redundancy: currently version strings are used in doc.conf and odmltables/__init__

[tables] find out which odML tags are not yet supported and check whether they can be easily integrated, 
to ensure full odml files when they are saved again.

[tables] find out if link/include are resolved and if not, resolve them before starting the wizard functionality 
to make sure no information is lost.  

[tables|1.0|core 1.4|py3|mergewiz] On startup `AttributeError`

[tables|1.0|core 1.4|py3|filterwiz] After select input file: `KeyError: SectionName`

[tables|1.0|core 1.4|py3] Any select file dialog opens in the background.

[tables|1.0|setup] When doing pip install, the PyQt5 dependency is not installed since its an extra dependency

[tables|1.0|Readme] Add PyQt dependency to the install notes in the readme 

[gin] re-direct after login does not work; re-directed to dashboard instead.

