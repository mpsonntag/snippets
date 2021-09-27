### Visualize Python code complexity

- Pylint features pyreverse
- requires graphvis

- installation in conda environment; python 3.9
```bash
pip install pylint
conda install -c anaconda graphviz
```
- run on a package
```bash
pyreverse -o svg -p [OutputName] [package]/
```

#### Link list

- https://www.logilab.org/blogentry/6883
- https://github.com/vidarh/diagram-tools/tree/master
- http://hokstad.com/making-graphviz-output-pretty-with-xsl-updated
