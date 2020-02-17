------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Python linters

flake 8, pylint, mypy, pycodestyle

pylint: ignore specific modules when checking file

pylint --extension-pkg-whitelist=lxml [filename]

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

# Different variants to test install

    python setup.py install --prefix=$INSTALL_DIR

    python setup.py install

    pip install .

    pip install --user .

    python -m unittest discover test

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

# Python packaging:

https://packaging.python.org/tutorials/distributing-packages

Create distribution from source:

    python setup.py sdist

This creates an archive file containing all source files and all additional files specified via the MANIFEST.in and setup.py specifics.

Naming conventions for upload: probably a good idea, to use versioning schemes like 1.3.1.1; 1.3.1.2; 1.3.1.3 etc for testing purposes. This has to be done, since if a bug in this specific release has to be fixed the bugged release file has to be removed from PyPI and only a fixed file with A DIFFERENT NAME can be uploaded, even if the first file has been removed!

IMPORTANT: use this naming scheme ONLY ON TEST PYPI. Once everything is tested and done,switch the name of the file from e.g. 1.4.2.2 back to 1.4.2 before uploading to PyPI proper!

update the python packaging description - still use x.y.z.# for pypi test package upload, but make sure that the version number in info.json and in the final upload to pypi proper is exactly the same e.g. 1.4.4 == 1.4.4 in the uploaded filename. otherwise pip install with supplying a specific version number will raise problems! e.g. odml==1.4.4 cannot be installed, if the uploaded file is named odml.1.4.4.2

This should of course not be done once we move on to the real PyPI release!

Check whether README.rst renders correctly in general:
http://rst.ninjs.org

Check whether the README.rst will be rendered correctly on PyPI

    pip install readme_renderer
    python setup.py check -m -r -s

NOTE: If the setup.py::licence attribute contains more lines or blank lines, then the description will NOT be displayed on PyPI but does not show up as an error. 
This might be true for other attributes as well.

Run the following check to ensure that the readme can properly be integrated in PyPI:

    twine check dist/*

Check [here](https://packaging.python.org/guides/making-a-pypi-friendly-readme/#validating-restructuredtext-markup) 
for more details.

## Check the documentation:

    sphinx-build -b html [sourcedir] [builddir]

For readthedocs: a project needs a setup.py to make sure, all dependencies are there.
Otherwise the documentation will not be properly built.

## Test Package

https://packaging.python.org/guides/using-testpypi/
https://testpypi.python.org
https://test.pypi.org

Upload the package to the PyPI test page to check whether everything required has been packed.

    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

Packages can be removed from the test server, but its neither nice, nor fast. Indices might take some time to update after a delete and a new upload.

## Test the Test Package

    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml

    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml-ui

if on conda, make sure to get the deps first:

    conda install -c pkgw/label/superseded gtk3 -y
    conda install -c conda-forge pygobject -y
    conda install -c conda-forge gdk-pixbuf -y
    conda install -c pkgw-forge adwaita-icon-theme -y


# Upload working package to PyPI proper (see below if making a release makes sense as well)

NOTE: make sure the dist folder contains ONLY the single package that is supposed to be uploaded. And not any .egg files etc.

    twine upload dist/*

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## Create git tag with corresponding version if required

creating a release:

- if necessary, update readme files.
- create branch with the version number e.g. v1.4

- check previous git tags:

    git tag -ln

- create a tag with the exact version number, pointing at the latest commit in the version branch.
    Note: This way, bugfixes from master can be cherry picked into the version branch and additional releases based on this branch can be, well, released.

    git tag -a v1.4 -m "tag message"

- push branch and tag upstream

    git push upstream v1.4

- create release featuring the created tag on github.
