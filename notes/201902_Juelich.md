## 05.02.2019 (09:00 - 18:00 / )

- gnode: Juelich security details (30')
- gnode: odMLtables paper updates (30')
- gnode: reading into SnakeMake and available continuous integration projects (2h)
- gnode: discussion with Robin Gutzen, Julia Sprenger regarding SnakeMake use case (1h30)
- gnode: discussion with Michael Denker, Julia Sprenger regarding SnakeMake project outline (3h)
- gnode: chat with Achilleas Koutsou regarding git/annex functions in SnakeMake (30')
- gnode: discussion with Michael Denker regarding Google Summer of Code (1h)
- gnode: presentation preparation ()


### Presentation:

Data hosting with GIN - Present and Future

Michael Sonntag
G-Node, LMU Munich (German Neuroinformatics Node)

06.02.2019, FSZ Juelich



Handling neuroscientific data with GIN - Present and Future

The German Neuroinformatics Node has been developing tools
for consistent storage, annotation and sharing of 
neurophysiological data and metadata.

This talk briefly introduces the metadata format odML and the 
raw-to-analysis data format NIX as well
as the developed data hosting and sharing platform GIN and its ecosystem
and gives an outlook on planned development of all projects with the
call for comment, feedback and feature requests.



#### A brief introduction of the G-Node

Funded by BMBF, hosted by LMU

Focusing on software tool development for

- storage     |
- annotation  |  of neurophysiological data
- sharing     |


www.g-node.org


#### Data formats developed by the G-Node

- odML (open metadata annotation language)
- NIX (Neuroscience exchange format)


www.g-node.org/NIX


#### Meta data storage format odML

- flexible metadata storage
- machine write and readable
- terminologies
- graphical user interface
- odMLtables plugin

github.com/G-Node/python-odml
github.com/G-Node/odml-ui
github.com/INM-6/python-odmltables

#### Latest odML format developments

- streamlined data format
- added support for YAML and JSON
- added export to RDF
- prototyped odML flavored RDF Apache Jena server
- prototyped abstracted SPARQL language for easy access


#### Data storage and data annotation with NIX

- based on hdf5
- data with metadata
- storing multiple analysis steps within the same file
- tagging of features of different 


#### NIXView

github.com/bendalab/NixView


#### Latest NIX developments

- format consolidation
- suite of tools for conversion[1]
- visualization tools easy integration into jupyter notebooks[2]
- NIXRawIO

[1] github.com/G-Node/nix-odml-converter
[2] github.com/G-Node/nixworks


#### GIN - G-Node Infrastructure

- based on git and git-annex
- web interface by adapting gogs
- workflow integration via command line client

gin.g-node.org


#### GIN features

- public / private repositories
- organizations and collaboration
- extensive user documentation
- in-house installation


#### GIN client

- Linux, Mac and Windows
- GIN-UI; graphical gin-cli wrapper on Windows


#### Web GIN features

- Elastic search
- odML integration
- NIX integration (upcoming)


#### GIN microservice architecture

- DOI service
- Format validation service (prototype)
- Continuous Integration service (upcoming)







[ToDo] should we post a "when you want to apply for this project, setup your own local instance of
gin-gogs, gin-valid and local gin-cli and get it to communicate"? then we already pre-select 
and have people that have an environment set up at the start of the project.





### GSoC SnakeMake project

#### INM-6 SnakeMake projects

- Julia Sprenger/Robin ??: analysis pipeline project
    analysis data to result nix file via SnakeMake?
- Julia Sprenger/Robin ??: odML refactoring pipeline via SnakeMake




#### Outline

- gin - PR
- hook to gin-ci
- gin-ci (go / python) receives clone request for repository on behalf 
    of the requesting user.
- gin get [repo]
- check existence root folder "SnakeMake" containing file "Snakefile", abort otherwise
- [how are required dependencies handled with SnakeMake]
- [how can we deal with already run parts of a SnakeMake run]
- [how do we ]
- [what should be returned to the user?]
  - service should provide a logfile for the latest run of a repo (security?)
  - output files? how should they be made available?
    pushed back to the repo?
    force pushed to its own results branch?
  - how to present results?



### which CI to use


Concourse
https://concoursetutorial.com/

Pros:
free
garbage collection scheme of finished jobs
gogs integration
extensive documentation and tutorials

neg:
relatively new, might not be as established/feature rich as other projects


Jenkins
https://jenkins.io/blog/2018/04/25/configuring-jenkins-pipeline-with-yaml-file/

pros:
free
established
extensive documentation and tutorials

neg:
huge
not as easy to adopt for users as other projects might be
uses groovy as build file syntax (not sure if yaml is supported)


Drone CI
https://medium.com/@jccguimaraes/run-a-drone-ci-pipeline-locally-f4bfb4741c53


pros:
gogs integration

cons:
might not be as free as we want
not much there in terms of documentation




