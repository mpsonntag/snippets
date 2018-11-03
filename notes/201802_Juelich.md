version handling
- where to put version string? currently in both __init__ and doc.conf; should be harmonized
- odmltables: use v0.1.1 for python 2 to 3
- odmlui: update version number of odmltables requirement to 0.1.1 and make release 1.3.1
    - release needs to contain single monitor fix

- odmltables: use v1.0.0 for odml-core v1.4 (which other issues should be addressed for this version?)
- odmlui: update version number of odmltables requirement to 1.0.0 for release 1.4.0

- terminologies: add check whether there is an internet connection and act appropriately if there is none.

- PyPI release plan for odmltables?

for our projects as well: why not try option2: from builtins import str as text

- issue: mac odml-ui pip install broken - fixed in 1.3, but default size commits need to be cherry-picked to development
- on conda mac saving a document crashes the application with a Glib-GIO Error: No GSettings schemas are installed on this system

- python-odmltables: check examples for v1.3 code that needs to be updated to 1.4

python-odml: doc.itervalues: in 1.4 returns just the values w/o any object information ... quite useless ... should this be refactored to return all properties to emulate the functionality from before where it returned the Value objects and therefore entrypoints into the odml tree from the value perspective? or remove and just use iterproperties

- _merge_odml_values in odml_table needs to be rewritten.


We, 07.02.2018, 08:00 - 19:00 (11h)
- travel to juelich
- fixing python3 compatibility in odmltables

Th, 08.02.2018, 09:00 - 20:00 (11h)
- Marseille Collab Group meeting of the Gruen Lab regarding their new project and the usage of gin, nix and odml within the project.
- discussion with Sonja Gruen regarding odml convergance, usage of nix and odml; possible inclusion of odml in HBP.
- discussion with Michael Denker regarding next steps with the Marseille project and the involvement of G-Node:
    they would be much obliged, if we get in touch with them on a regular basis for updates on their end and if they need any assistance with the G-Node software.
- discussion with Ljuba Zehl regarding using nix/odml in one of her new projects and a potential workshop with her in Munich, if both her boss and the G-Node would support this with time and effort.
- fixing python 3 compatibility issues in odmltables
- fixing odmltables tests for both python 2 and python 3
- setting up continuous integration for odmltables

Fr, 09.02.2018, 09:00 - 18:00 (9h)
- testing odml versionconverter with juelich odmlfiles ... there are no obvious problems
- converging odmltables with odml v1.4 - there are quite some changes that need to be made to deal with the removal of odml values. first steps have been taken, but quite a lot of changes still have to be made.
- accomodastion reimbursement with Juelich

Su, 11.02.2018, 08:30-09:00 (30min)
- fixing tests in odmltables

Mo, 12.02.2018, 08:30 - 09:30 (1h)
- nachbereitung juelich
- fixing tests in odmltables

Juelich Notes:
- possible problems for us: when odmltables saves an odml, this odml is not a full fledged odml file ... various tags will not be exported e.g. repository, include or link ... this also means, that includes are not used when filtering, merging etc an odml file, that does not come from juelich. - add a resolve link/include function at the start of every odmltables wizard, to make sure, that all possible information is there.
- add value_origin + other easy fields that are currently not supported to make the resulting odml files closer to the original odml format.

Tu, 13.02.2018, 09:00 - 09:30
- PR reviews


- all print statments are p3 compatible
- no py2 style raise
- [td] catching exceptions ... not sure about StopIteration() in except clause
- [td] division: mainwindow:96 division could differ between 2 & 3 but should not be tragic
- long integers: long escaped by using past.builtins
- backtick repr: no occurrence
- metaclass: no occurrence
- [td] unicode literals: doc.conf contains u'' notated unicode strings. should be fine.
- [td] byte string literals: looping over byte string could be hidden in the code and not be properly escaped.
- basestring usage: no occurrence
- [td] unicode: two usages
    - could try from builtins import str as text option to avoid unicode `try /* ... */ except /*...*/`
    - [done] weird usage in odml_xsl_table:309-310 ... uses unicode first, str second
- stringio: no occurrences
- [done] package imports: might need a second step to make all imports relative (gui part, tests when importing from odmtables package)
- iterkeys: no occurrences
- [done] itervalues: odml_table:79 import of itervalues() might be changed to from builtins import itervalues, but must check if works with py2 and 3
- [td] iteritems: should be resolved, but resulting (k,v) should be wrapped in brackets
- [done] dict keys as lists: works, but could be inefficient on py2; odml_table, odml_xls_table, filterpages,
- [done] dict values as lists: same as above: odml_csv_table, odml_table, generatetemplatepages, filterpages, converterpages - use slow version for now
- [done] dict items as lists: same as above< odml_table, converterpages, pageutils - use slow version for now
- custom iterators: no occurrence
- custom __str__ methods: no occurrence
- custom __no_zero__ methods: no occurrence
- xrange: no occurrence
- [td] range: occurrences in: example3, odml_csv_table, create_examples, odml_table, compare_section_xsl_table, compare_section, ...
- map: no occurrence
- imap: no occurrence
- zip: multiple occurrences but no description how to fix it - check whether there are differences in 2 and 3
- reduce: no occurrence
- raw_input, input, file: no occ
- tests run with py 2 and py 3
