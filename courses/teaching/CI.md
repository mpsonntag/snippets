# github actions

Main information from the official [github actions documentation](https://docs.github.com/en/actions).

## General introduction

- github actions are event driven
- when a specified event on github occurs e.g. a pull request, a workflow is triggered.
- a workflow contains a specific job
- each job bundles specific actions and the order in which these actions are executed
- the actions include
  - testing
  - building
  - packaging
  - creating releases
  - deploying on github
- actions are standalone building blocks that can be bundled in a job; they can also be created from scratch and shared within the community

- the workflow is added by a user to the repository

## Virtual environments

Jobs can be run in the following environments:

Virtual environment     YAML workflow label
Windows Server 2019     windows-latest
                        windows-2019
Ubuntu 20.04            ubuntu-20.04
Ubuntu 18.04            ubuntu-latest
                        ubuntu-18.04
Ubuntu 16.04            ubuntu-16.04
macOS Big Sur 11.0      macos-11.0
macOS Catalina 10.15    macos-latest
                        macos-10.15

Check the following page which software packages [are available](https://docs.github.com/en/actions/reference/specifications-for-github-hosted-runners).


# appveyor


