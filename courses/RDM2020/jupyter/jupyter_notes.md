Run the jupyter notebook

    jupyter nbconvert BIDS_introduction.ipynb --to slides --post serve

When running the jupyter notebook, it will create a *.slides.html file. use that one in presentations and for handouts.
Use the following command to create a static html page and then convert that one manually to pdf:

    jupyter nbconvert --to html BIDS_introduction.ipynb

