# G-Node project workflow and handling etiquettes

### git workflows

- make changes only in your fork
- setup remotes (origin and upstream)
```bash
git clone git@github.com:username/reponame.git
cd reponame
git remote add upstream git@github.com:G-Node/reponame.git
git remote -v
git fetch --all
```

- we usually do not `git pull` or `git merge`
- use the following workflow
```bash
git fetch --all
git rebase upstream/master  # or appropriate branch
git checkout -b [branchname]
# run tests locally
# run linters locally
git commit -m "[affected file] Short description, max total length 50 char"
git commit --amend  # extensive description if appropriate
git push origin [branchname]
```
- then open a pull request (PR) from origin [branchname] to upstream [master] (or appropriate branch)

- never force push upstream! only ever force push to your own fork


### git commit etiquette

- try to keep commits small
- try not to commit changes that break code
- do not mix code changes e.g. changes in two unrelated functions or cleanup and functional change; makes it easier to document why which change has happened or identify when an issue has occurred.
- keep commit message subjects below 50 characters - makes the history easy to read and informative
- here is a good article about git [commit messages](https://chris.beams.io/posts/git-commit/)

- phrase the comment bodies so that they can be re-used as Pull Request description 
- if possible, use square brackets at the beginning of the message to indicate which file has been modified. Find examples [here](https://github.com/G-Node/gin-doi/pull/128/commits/6623a1c0609d73169c5039dde750daed890b58df) and [here](https://github.com/G-Node/gin-doi/pull/128/commits/47dbcb5c6af816ce97f8aaf13cededc4037168bb).


#### Smooth commit handling

On Linux, you can add the following to your `.bash_alias` file and use as `gitcom "Add commit message"`
instead of `git commit -m "message"` to ensure appropriate message length:

```bash
alias gitcom='function __gitcom(){ if [[ "${#1}" > 50 ]]; then echo "Commit message too long: ${#1} chars"; else git commit -m "$1"; fi }; __gitcom'
```


### github issue etiquette

- create issues on the upstream repository
- check if there already is an issue to the point you want to raise
- when writing the issue
  - keep the title short
  - do not use titles that spill over into the content body
  - never create an issue with an empty content body
  - try to be as descriptive as possible
- ideally add full code examples how an issue can be reproduced.
  example: https://github.com/G-Node/nixpy/issues/527
- if there is a related issue, refer to it: typing `#123` will automatically refer to issue 123
- for feature request issues make sure it is actually a single feature. If there are actually more features, create more issues.


### Pull Request (PR) etiquette

- if possible keep the PRs reasonably small (morale boost for the reviewers when they do not have to read 400+ lines of code...)
- list all points that are addressed - if the commit description is thorough, use it
- refer to the issues it addresses - typing `#123` in the text will automatically refer to issue 123
- you can also refer to other PRs via this running counter
- at first document if tests have passed with which version of a programming language and linters have been run until this becomes second nature before pushing in the first place.
- check an opened Pull request after a while whether all the tests and checks have succeeded.
- if there are issues, fix them and push the commits to the same branch; the PR will be updated automatically
- PRs that show CI issues will not be reviewed.
- if reviewers have requested changes, either push more commits to address these changes or comment directly on the points that were raised so that any discussion is visible and documented.
- find a general PR example [here](https://github.com/G-Node/python-odml/pull/389) and a PR example with extensive reviews and discussion [here](https://github.com/G-Node/nixpy/pull/495).
