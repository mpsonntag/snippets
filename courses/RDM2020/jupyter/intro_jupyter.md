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

# Package managers and virtual environments

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

