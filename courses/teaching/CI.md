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

## Reference workflow

github action workflows are provided in a git repository as yaml files at a `.github/workflows` directory. 

    # distinguish different workflows, the name can be freely chosen; this name is displayed on github
    name: human-readable-name
    # define when this workflow should be executed on github
    # multiple actions can be chosen
    # available actions are: push 
    on: [push]
    # list of jobs that are run
    jobs:
      # each job can have its own name and can be freely chosen
      job-1:
        # multiple operating systems can be chosen; see above which labels are available
        runs-on: ubuntu-latest
        # steps is a grouping container for all steps
        steps:
          # via 'uses' the step will fetch the defined action 'actions/checkout' at version 'v2'
          # this action downloads the repository to the runner environment
          - uses: actions/checkout@v2
          # actions can also be named; the following action will setup python
          - name: Setup Python 3.8
            uses: actions/setup-python@v2
            with:
              python-version: 3.8
          # run executes a command on the runner, can also be named
          - name: Display installed Python version
            run: python -c "import sys; print(sys.version)"


# appveyor


