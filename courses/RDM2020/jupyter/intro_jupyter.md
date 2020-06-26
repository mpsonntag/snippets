# Introduction to Jupyter notebooks

Today's session will be brutal in terms of information I am going to throw at you but potentially very rewarding with respect to concepts, tools and useful resources you can get out of it.
As a scientist you are expected to be independent find out the things you need on your own. We expect that as well. Most of the work you will have to do on your own. You will have to experiment! With the tools and with your workflows that come out of it. But we will give you a head start by exposing you to the most important concepts and tools, how they best fit together and which resources are best to get going with them.

Show of hands who knows
- how to script with Matlab
- how to script with Python
- how to script with R

- jupyter notebooks
- conda

## Overview Jupyter notebooks
- reconcile code and documentation using the browser
  - like a labbook for code and plots
  - easy to view and hand over
- can be used with different scripting languages
  - Python
  - R
  - (Matlab)
- has tools built around it
  - can be used for presentations
  - can be shared and read online using nbviewer
  - can be shared, run and modified online using binder

Find a short introduction at 
- https://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb

# Detour: Package managers and virtual environments

A package manager
- keeps track of installed software packages
- provides a list of available software packages
- enables a user to install available software packages from available off-site repositories
- different ones exist for OS system packages or programming language libraries

A virtual environment
- is a tool that keeps software packages separate from the operating system.
- can be used to install different versions of the same software.
- can be used to document and re-create and share an analysis environment.

(Ana)Conda is a cross platform package manager and a virtual environment.

## Conda installation and resources

Installation files and instructions
https://docs.conda.io/en/latest/miniconda.html

20 minute introduction to conda
https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

Conda commands cheat sheet
https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf

## Working with conda
- open a terminal
- create a new conda virtual environment
    conda create -n [env_name] python=3.8

- activate the environment
    conda activate [env_name]

- install software packages using the conda package manager - will be installed into the active environment only
    conda install [library]

- install python packages using pip; when using pip, it will be installed into the active environment only
    pip install [library]

- deactivate an active environment
    conda deactivate

- delete an environment with all installed software packages
    conda remove -n [env_name] --all

Pitfall: Do not use `conda activate`. Immediately do `conda deactivate`. Otherwise the installation of conda will be affected and can become unusable.

## Conda and Windows

Conda terminal: from the Start menu, search for and open "Anaconda Prompt."

Known issue: whitespace - path issue
- https://github.com/conda/conda/issues/8725
- https://docs.anaconda.com/anaconda/user-guide/faq/
"
In what folder should I install Anaconda on Windows?

We recommend installing Anaconda or Miniconda into a directory that contains only 7-bit ASCII characters and no spaces, such as C:\anaconda. Do not install into paths that contain spaces such as C:\Program Files or that include Unicode characters outside the 7-bit ASCII character set. This helps ensure correct operation and no errors when using any open-source tools in either Python 3 or Python 2 conda environments.
"

# Finally: Jupyter notebooks

https://jupyter.org/

"Project Jupyter exists to develop open-source software, open-standards, and services for interactive computing across dozens of programming languages."

- all Jupyter notebooks require a Python installation
- Python is the default scripting language in Jupyter notebooks

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

## Python Libraries

The most important ones and how they can be installed

pip install jupyter
pip install ipython
pip install numpy
pip install matplotlib

Widgets; interactive Jupyter notebooks
- https://www.mikulskibartosz.name/interactive-plots-in-jupyter-notebook/

## Installation example of Jupyter in a conda environment

- open a (conda) terminal
- create the python conda environment


    conda create -n jnb-py38 python=3.8 -y

- activate the environment


    conda activate jnb-py38

- install jupyter into the active conda environment


    pip install jupyter

- navigate to a directory on you operating system where you want to save files or have datafiles you want to use


    cd [path/to/working/directory]

- open jupyter


    jupyter notebook

- automatic switch to the browser
- select "New -> Notebook: Python3"
- will open another tab with an unsaved notebook
- save the notebook

- to close a notebook, switch to the terminal
- press "ctrl+C" ("cmd+C" on macOS)

- you can directly start an existing notebook from the command line


    jupyter notebook [file_name.ipynb]

## Using Jupyter notebook

Check the reference for FAQs and details
- https://jupyter-notebook.readthedocs.io

Find a quick tutorial about the basic features here
- https://realpython.com/jupyter-notebook-introduction

We'll do a quick feature glimpse on a live Jupyter notebook.

## Markdown (see Lecture05)
- https://www.markdownguide.org/cheat-sheet
- https://guides.github.com/features/mastering-markdown/

## Make your life easier - use keyboard shortcuts

The running notebook provides a full list of available shortcuts via the notebook menu:

    `Help` -> `Keyboard Shortcuts`

You can also find a reference here
- https://jupyter-notebook.readthedocs.io/en/stable/notebook.html?highlight=shortcuts#keyboard-shortcuts

Nice rundown also comparing across OS platforms can be found here
- https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330

## Make your life easier - use magic methods

Jupyter specific magic methods (subset of Python magic)
- https://nbviewer.jupyter.org/github/ipython/ipython/blob/6.x/examples/IPython%20Kernel/Cell%20Magics.ipynb

Python magic methods
- https://ipython.readthedocs.io/en/stable/interactive/magics.html

## Use Jupyter notebooks as presentations

In a running notebook:

    `View` -> `Cell toolbar` -> `Slideshow`

You can now select how each cell should appear in a presentation.

After you have saved your notebook and closed Jupyter, restart Jupyter as a presentation tool:

    jupyter nbconvert [file_name.ipynb] --to slides --post serve

When running the jupyter notebook, it will create a *.slides.html file. use that one in presentations and for handouts.
Use the following command to create a static html page.

    jupyter nbconvert --to html BIDS_introduction.ipynb

The HTML file can then be converted to a PDF and handed around.

## Additional features when publishing notebooks

Uploading Jupyter notebooks to public git repositories gives access to additional tools

- can be published on any online git repository e.g. github, gitlab, gin ...
- online viewing of notebook content via NBViewer
    https://nbviewer.jupyter.org

Example
https://github.com/G-Node/nix-demo/blob/master/2019_RDM_course_nix.ipynb

- online editing via Binder

# Binder

Binder is a free service that enables to run a published Jupyter notebook on a remote machine.
With minimum set up you can run and work on a full Jupyter notebook without the need to install the environment locally.

The full documentation in how to properly use Binder can be found here
- https://mybinder.readthedocs.io/en/latest/

You can find minimal examples how to set up a repository for use with binder for Python and R at
https://github.com/binder-examples

We will do a very quick introduction into how to set up and use a Python and an R Binder notebook

## Empty Python Binder set up

Prepare an empty, public git repository
To start a Python Jupyter notebook via Binder you need to provide two files at the root of the repository.
- `runtime.txt` ... this file contains the Python version that will be used for any Notebook started by this repository. It contains only one entry:

    python-3.8
- `requirements.txt` ... this file contains the Python packages that will be installed when the container starts. In our example we will install the following python packages:

    numpy
    matplotlib
    nixio==1.5.0b4

Commit and upload these files to the public git repository

Go to https://mybinder.org/
Select `Git repository` and paste the URL of the repository e.g. https://gin.g-node.org/msonntag/demo
Select `launch`; it will now take a bit until the environment is created and ready for you to use.
You can now create a new notebook vie the menu `New -> Notebook: Python3`.
A new tab will open and you can save it under a new name - this will still be on the remote machine.
You can always save the notebook to your local machine via the `Download` menu button.
You can now work on this notebook as you would locally.

## Python Binder with an existing notebook

As above you have to set up a git repository with the environment and the Python dependencies
Also upload the existing Jupyter notebook to this repository and also any data files you want to use in this notebook
Again go to https://mybinder.org and set up the repository information as before.
But now also provide the file name of the uploaded Jupyter notebook and select `Launch`
Binder will now launch the notebook directly.

Note that
- https://mybinder.org also provides a permanent link to such a notebook

## Notes on Binder

Binder is a free service
- building a container might take up to 20min the first time around.
- takes longer the more dependencies are defined.
- built containers are kept for a while - the next time the Binder is used, the start up will take less time.

Binder is a cloud service; all files are remote
- upload required dependencies and files to the git repository
- upload required files to the running cloud service
- save changes to your notebook in the cloud service AND download the notebook to your local machine
- Binder will time out when there is inactivity - save OFTEN

https://mybinder.org provides a permanent link to public binder git repositories
- you can run your notebook from anywhere
- collaborators can easily run your notebook as well

You can have multiple Jupyter notebooks in the same directory
- all can have their own permanent links
- all will share the same environment and dependencies

# Jupyter and R

## Full example of Jupyter with R in conda

kernel ... enables the notebook to understand R syntax

    conda create -n r-jnb-py38 python=3.8 -y
    conda activate r-jnb-py38
    conda install -c conda-forge jupyterlab -y
    conda install -c r r-base -y
    conda install -c r r-irkernel -y

    jupyter notebook

From the menu select `New -> Notebook: R`

## Additional resources to set up Jupyter with R

Jupyter and R - setup and use
- https://www.datacamp.com/community/blog/jupyter-notebook-r
- https://datatofish.com/r-jupyter-notebook/
- https://plotly.com/r/using-r-in-jupyter-notebooks/

R maintains its own channel on conda and provides all libraries for conda environments there
- https://anaconda.org/r

### Useful R libraries available via conda

`r-base` ... core installation
`r-tidyverse` ... package collection; https://tidyverse.tidyverse.org; it contains
- ggplot2, for data visualisation.
- dplyr, for data manipulation.
- tidyr, for data tidying.
- readr, for data import.
- purrr, for functional programming.
- tibble, for tibbles, a modern re-imagining of data frames.
- stringr, for strings.
- forcats, for factors.

Install it using

    conda install -c r r-base
    conda install -c r r-tidyverse


## R Binder set up example 

We again need a public git repository
This time we need to provide the YAML file `environment.yml` at the root of the repository.
It contains all `conda` packages that need to be installed to run the `R` Jupyter notebook in Binder.

channels:
  - r
dependencies:
  - r-base
  - r-tidyverse

Upload the file to the public git repository
Go to https://mybinder.org/
Select `Git repository` and paste the URL of the repository e.g. https://gin.g-node.org/msonntag/demo
Select `launch`; it will now take a bit until the environment is created and ready for you to use.
You can now create a new notebook vie the menu `New -> Notebook: R`. Note, that we also still have the Python dependencies in the same repository. That is why we could also start a Python3 notebook as well.
A new tab will open with the Jupyter notebook. Note the `R` logo which denotes that we are working in an R Jupyter notebook.

## Jupyter and Matlab

Matlab - live editor and Matlab online
- https://www.mathworks.com/products/matlab/live-editor.html
- https://www.mathworks.com/products/matlab-online.html

Matlab in Jupyter notebooks:
- https://anneurai.net/2015/11/12/matlab-based-ipython-notebooks

Matlab kernels for Jupyter notebooks
- https://github.com/Calysto/matlab_kernel
- https://github.com/imatlab/imatlab

## Jupyter notebooks and good practice

https://reproducible-science-curriculum.github.io/publication-RR-Jupyter/
