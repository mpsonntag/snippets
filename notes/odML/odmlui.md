------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

odml-tables/-ui integration:
ToDo
- use it under windows.
- being able to start it when ui is run with py3

        elif sys.platform == "windows":
            if os.system("where odmltables") == 0:
                has_tables = True

            if not has_py2 and os.system("which python2") == 0:
                has_py2 = True

            # start odml tables
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                os.system("odmltables &")

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

odmlui conda MacOS Gtk issue
https://developer.gnome.org/gio/stable/glib-compile-schemas.html
http://linuxfromscratch.org/blfs/view/svn/general/glib2.html

https://stackoverflow.com/questions/24370294/glib-gio-error-when-opening-an-file-chooser-dialog
https://stackoverflow.com/questions/28953925/glib-gio-error-no-gsettings-schemas-are-installed-on-the-system
https://stackoverflow.com/questions/9678301/can-not-use-gtk3-filechooser-on-mac-osx
https://stackoverflow.com/questions/37916185/how-to-fix-error-glib-gio-error-no-gsettings-schemas-are-installed-on-the-sy
https://stackoverflow.com/questions/37454358/how-to-configure-gsettings-for-gnome-and-gtk

MacOS print current environmental variables:

        printenv

Temporarily set environmental variable on MacOS

        export VARNAME=bla

To unbreak the filechooser:

    export GSETTINGS_SCHEMA_DIR=$CONDA_PREFIX/share/glib-2.0/schemas

usually the glib2 schema is found in 

    $(conda_environment_folder)/share/glib-2.0/schemas
    
    e.g. with user "peter" and odmlui installed in conda environment "odml"
    /Users/peter/conda/envs/odml/share/glib-2.0/schemas


https://conda.io/docs/user-guide/tasks/manage-environments.html#macos-linux-save-env-variables

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Fixing background terminology errors

class EditorTab(object):
    """
    Represents a Document Object in the Editor
    """
    file_uri = None
    edited = 0

    def __init__(self, window, cmdm=None):
        if cmdm is None:
            cmdm = CommandManager()
            cmdm.enable_undo = self.enable_undo
            cmdm.enable_redo = self.enable_redo
            cmdm.error_func = window.command_error
        self.command_manager = cmdm
        self.document = None
        self.window = window
        self._clones = [self]

    def new(self, doc=None):
        """
        initialize a new document
        """
        if doc is None:
            doc = odml.Document()
            sec = odml.Section(name="Default Section")
            doc.append(sec)

        # TODO Was the following commented line missing on purpose?
        # If values are not there the display shows grey, maybe there
        # is supposed to be a difference between sthg loaded from
        # terminologies and the other stuff, but the current implementation
        # leads to tons of errors in the background.
        # self.parse_properties(self.document.sections)

        self.window.registry.add(doc)

        self.document = doc
        self.file_uri = None

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Gtk icons in conda environment

gtk.IconTheme.get_default().get_search_path())
gtk.IconTheme.get_default().has_icon('document-new')
gtk.IconTheme.get_default().has_icon('gtk-new')
gtk.IconTheme.get_default().prepend_search_path(path)

-----------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

conda empty test:
    conda create --name emptyPy2 python=2.7

activate, try install, test gi import error
    conda install -c conda-forge pygobject

try install, test atk import error
    conda install -c conda-forge atk pango

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

line 987 in editor ... make sure an appropriate object is selected when an object is removed.

We have
- treeview

self.get_focus() ... returns active part of window ... widget ... e.g sectionView or propertyView 


On document load of a document with a section and no properties:

_property_tv
    _section ... None
    model ... None
    section ... None
    _treeview ... Gtk.TreeView

_property_view


Editor: on_load
EditorTab: init
EditorTab: load
    self.document = odmlParser document
    self.document.finalize()
Helpers:
    # Every odml-ui property requires at least one default value according
    # to its dtype, otherwise the property is currently broken.
    # Further the properties are augmented with 'pseudo_values' which need to be
    # initialized and added to each property.
    for sec in self.document -> handle_section_import -> handle_property_import -> create_pseudo_values
Editor: self.append_tab

Candidate:

Object removal and icon display fixes

This PR 
- Fixes background errors when deleting Properties or Document root Sections. Closes #99.
- Fixes various occasions where the "Add Property" and "Add Value" icons were not 
    properly deactivated. Closes #90.

-----------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Issues

- odml-ui: make datatype default values user defineable
- odml-ui: remove encoder, filename, etc.
- odml-ui: are shortcuts documented somewhere? how do they work under mac?

- [ui|import] error when importing an 1.1 version file.

- [ui|import] No proper error message when an import fails due to e.g. link and include in the same section

- [ui|main] check odml version on startup and give intelligible error message on old version.

- [ui|Editor] File menu "Open recent" does not display errors compared to opening from the dashboard.

- [ui|Editor] Add info texts for section and property attributes in the attributes view.

- [ui|Editor] Attribute frame: info icons + text for include, link and dependency value

- [ui|Editor] Change the window size to show all potential section/property attributes w/o manual resizing

- [ui|Editor] If possible add shortcut F2 to edit something

- [ui|terminology] Handle terminology loading fails
    Repositories of an open odml document are loaded in the background. If a repository link 
    fails to be loaded, it will try again. And again and again and again and again and again 
    and again and again and again and again and again and again...

- [ui|TreeIters] Should some of the content of get_value:L57 not better be moved to
        ValueModel#get_display() ?

- [ui|AttributeView:L66] cgi.escape deprecated, use html.escape instead

- [ui|Info Bar] Message display times:
    - the message display times are too short.
    - some messages e.g. errors should not go away without a user action.

- [ui|1.3 only?] When loading a file using the FileChooser and the loading fails, it fails in the background
    w/o closing the FileChooser and w/o providing an error message.

- [ui|text.py|1.4] xmlparser.XMLReader.fromString is used in text.py and needs to be replaced with from_string.

- [ui|PropertyView] Uncertainty should maybe only be available for entry, if the value is numeric.

- [ui|Wizard] Terminology usage
    - Use terminology repo url from odml-core as default url
    - Properly use Terminology class and clean up after the wizard is done before it closes. (but that does not help, because
        the core lib does deferred load of whichever instance every time a repository is touched.)

- [ui|wizard] One can actually rename terminology section names in the select list - is that what we want?

- [ui|wizard/validation] the standalone functions could be removed, 
    ... since they are not functional with the relative imports anyway.

- [ui|wizard] Terminology section save info
    Add info that only sections that are modified will be saved to file when loading sections from a terminology.

- [ui|version 1.4.0] Update version number of odmltables requirement to 1.0.0 for release 1.4.0

- [ui|version 1.3.1] update version number of odmltables requirement to 0.1.1 and make release 1.3.1; 
    release needs to contain single monitor fix as well

- [ui] check PyPI release for PyGObject
    https://pygobject.readthedocs.io/en/latest/getting_started.html#pypi
    https://lazka.github.io/pgi-docs/

- [ui] for windows: prerequisites
    https://sourceforge.net/projects/pygobjectwin32/
