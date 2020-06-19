# Introduction to jupyter notebooks

Today's session will be brutal in terms of information I am going to throw at you but potentially very rewarding with respect to concepts, tools and useful resources you can get out of it.
As a scientist you are expected to be independent find out the things you need on your own. We expect that as well. Most of the work you will have to do on your own. You will have to experiment! With the tools and with your workflows that come out of it. But we will give you a head start by exposing you to the most important concepts and tools, how they best fit together and which resources are best to get going with them.

## Take home message: why use jupyter notebooks

- reconcile code and documentation
  - like a labbook for code and plots
  - easy to view and hand over
- can be used for presentations
- can be used with different scripting languages
  - Python
  - R
  - (options for Matlab)

show of hands

who knows how to script with matlab
who knows how to script with python
who knows how to script with R

who knows virtual environments or conda
who knows ipython or jupyter notebooks
who knows markdown

## Introduction to Python

Not by me

Here are three links to lessons tailored for scientists; can each be done in 1/2 - 1 day:
- https://swcarpentry.github.io/python-novice-inflammation
- https://swcarpentry.github.io/python-novice-gapminder
- https://datacarpentry.org/python-ecology-lesson

They include
- Python essentials; fundamentals, functions, exceptions, debugging
- Data handling libraries
- Data loading, handling and plotting

## Jupyter notebooks

Example

## Markdown

Get reference sheet
https://www.markdownguide.org/cheat-sheet
https://guides.github.com/features/mastering-markdown/

- how to put images in

## Jupyter shortcuts

- https://jupyter-notebook.readthedocs.io

For the full list of available shortcuts, click Help, Keyboard Shortcuts in the notebook menus.

Nice rundown also comparing across OS platforms can be found here
- https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330

## Installation variants

Please bear with me if this is too much to take in; the option I propose at the end will be
easier to use, but it kind of depends on this information. And if you want to use python
locally as well, you should be aware of these options and the documentation links to solve the
issues you will encounter on your own.

pip (native, not recommended)
conda (with respect to OS adaption probably the best option)

## Python Libraries

The most important ones

ipython
jupyter
numpy
matplotlib
pandas

work with pip

work with conda

Conda and windows - whitespace - path issue
https://github.com/conda/conda/issues/8725

https://docs.anaconda.com/anaconda/user-guide/faq/

"
In what folder should I install Anaconda on Windows?

We recommend installing Anaconda or Miniconda into a directory that contains only 7-bit ASCII characters and no spaces, such as C:\anaconda. Do not install into paths that contain spaces such as C:\Program Files or that include Unicode characters outside the 7-bit ASCII character set. This helps ensure correct operation and no errors when using any open-source tools in either Python 3 or Python 2 conda environments.
"

widgets; interactive jupyter notebooks
https://www.mikulskibartosz.name/interactive-plots-in-jupyter-notebook/

## create a conda environment, install dependencies

`conda create -n work python=3.7`

`conda activate work`

`conda deactivate work`

`pip install [library]`

`conda install [library]`

`conda remove -n work --all`

Pitfall: Do not use `conda activate`. Immediately do `conda deactivate`

## Jupyter example

## NBViewer

https://nbviewer.jupyter.org/

## Internals

look at json

pitfall: jupyter and git

Save with vs without results

## Use it as a presentation tool

## Binder

Additional information at
https://mybinder.readthedocs.io/en/latest/


Binder will time out, if there is inactivity. in this case all changes are lost! if you want to work on a notebook, download frequently, because all changes will be lost when the container is shut down and recycled.

binder examples
https://github.com/binder-examples

## Jupyter and R

links how to install and use
- https://plotly.com/r/using-r-in-jupyter-notebooks/

most important libraries

## Jupyter and Matlab

Matlab - live editor and matlab online
- https://www.mathworks.com/products/matlab/live-editor.html
- https://www.mathworks.com/products/matlab-online.html

Matlab in jupyter notebooks:
- https://anneurai.net/2015/11/12/matlab-based-ipython-notebooks/

Matlab kernels for jupyter notebooks
- https://github.com/Calysto/matlab_kernel
- https://github.com/imatlab/imatlab
