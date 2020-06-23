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

Show of hands

who knows how to script with Matlab
who knows how to script with Python
who knows how to script with R

who knows conda
who knows ipython or jupyter notebooks

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

https://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb

## Markdown (already done by Thomas)

https://www.markdownguide.org/cheat-sheet
https://guides.github.com/features/mastering-markdown/

- how to put images in

## Jupyter shortcuts
- https://jupyter-notebook.readthedocs.io

For the full list of available shortcuts, click Help, Keyboard Shortcuts in the notebook menus.
- https://jupyter-notebook.readthedocs.io/en/stable/notebook.html?highlight=shortcuts#keyboard-shortcuts

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

Work with pip

Work with conda

Conda and Windows - whitespace - path issue
https://github.com/conda/conda/issues/8725

https://docs.anaconda.com/anaconda/user-guide/faq/

"
In what folder should I install Anaconda on Windows?

We recommend installing Anaconda or Miniconda into a directory that contains only 7-bit ASCII characters and no spaces, such as C:\anaconda. Do not install into paths that contain spaces such as C:\Program Files or that include Unicode characters outside the 7-bit ASCII character set. This helps ensure correct operation and no errors when using any open-source tools in either Python 3 or Python 2 conda environments.
"

Widgets; interactive jupyter notebooks
https://www.mikulskibartosz.name/interactive-plots-in-jupyter-notebook/

## create a conda environment, install dependencies

`conda create -n work python=3.7`

`conda activate work`

`conda deactivate work`

`pip install [library]`

`conda install [library]`

`conda remove -n work --all`

Pitfall: Do not use `conda activate`. Immediately do `conda deactivate`

A full script to install jupyter notebook in conda with relevant libraries


## Jupyter example

How to start one

```bash
jupyter notebook
```
or
```bash
jupyter notebook [notbook_name]
```

To shut it down again, type Ctrl+C

## Full example

conda create -n jnb python=3.8 -y
conda activate jnb
pip install ipython
pip install numpy
pip install matplotlib
pip install jupyter

jupyter notebook



## NBViewer

https://nbviewer.jupyter.org/

## Internals

Look at json

Pitfall: jupyter and git

Save with vs without results

## Use it as a presentation tool

`View` -> `Cell toolbar` -> `Slideshow`


## Binder

Additional information at
- https://mybinder.readthedocs.io/en/latest/

Binder will time out, if there is inactivity. in this case all changes are lost! if you want to work on a notebook, download frequently, because all changes will be lost when the container is shut down and recycled.

Binder examples
- https://github.com/binder-examples

## Jupyter and R

- https://www.datacamp.com/community/blog/jupyter-notebook-r
- https://datatofish.com/r-jupyter-notebook/

Links how to install and use
- https://plotly.com/r/using-r-in-jupyter-notebooks/

Most important libraries

## Jupyter and Matlab

Matlab - live editor and matlab online
- https://www.mathworks.com/products/matlab/live-editor.html
- https://www.mathworks.com/products/matlab-online.html

Matlab in jupyter notebooks:
- https://anneurai.net/2015/11/12/matlab-based-ipython-notebooks/

Matlab kernels for jupyter notebooks
- https://github.com/Calysto/matlab_kernel
- https://github.com/imatlab/imatlab
