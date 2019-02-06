## 05.02.2019, 09:00 - 18:00 / 22:00 - 00:30 (11h30)

- gnode: Juelich security details (30')
- gnode: odMLtables paper updates (30')
- gnode: reading into SnakeMake and available continuous integration projects (2h)
- gnode: discussion with Robin Gutzen, Julia Sprenger regarding SnakeMake use case (1h30)
- gnode: discussion with Michael Denker, Julia Sprenger regarding SnakeMake project outline (3h)
- gnode: chat with Achilleas Koutsou regarding git/annex functions in SnakeMake (30')
- gnode: discussion with Michael Denker regarding Google Summer of Code (1h)
- gnode: presentation preparation (2h30)


### Presentation abstract

Handling neuroscientific data with GIN - Present and Future

The German Neuroinformatics Node has been developing tools
for consistent storage, annotation and sharing of 
neurophysiological data as well as metadata.

This talk briefly introduces the metadata format odML and the 
raw-to-analysis data format NIX, will elaborate on their recent development
and refer to their integration into the data management platform GIN.

The introduction will further cover GINs main features of version control,
workflow integration to collaboration and data sharing as well as its 
ecosystem from data publication to content validation. An outlook on 
planned development raises a call for comment, feedback and feature requests.


## 06.02.2019, 09:00 - 18:00 (9h)

- gnode: presentation preparations (4h)
- gnode: Juelich presentation (1h)
- gnode: video conference with Jan Grewe, Michael Denker, Julia Sprenger re odmltables paper (1h)
- gnode: discussion with Michael Denker, Julia Sprenger regarding SnakeMake project outline (1h30)
- gnode: odmltables paper updates (1h)
- gnode: presentation cleanup on gin (30')




[ToDo] get updated NIX / odML / gin slides for presentations
[ToDo] overhaul the logOS, presentation etc folders on github and move stuff to gin



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


[ToCheck] SnakeMake ReadTheDocs remote filehandling iRODS ... timestamp problem handling

https://snakemake.readthedocs.io/en/stable/snakefiles/remote_files.html

It would be nice to have gin as another remote, so that we can fetch infiles from remotes
directly ... Michael Denker asked Johannes Koester whether someone is already working on a 
remote.




https://www.booking.com/hotel/de/keizerplatz-apartment.de.html




