## 05.02.2019 (09:00 - )

- gnode: Juelich security details (30')
- gnode: odMLtables paper updates (30')
- gnode: reading into SnakeMake ()



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




