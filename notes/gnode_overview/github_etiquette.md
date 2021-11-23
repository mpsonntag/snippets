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

- we usually do not `git pull` or `git merge`
- never force push upstream! only ever force push to your own fork

You can put the following in your .bash_alias file and use as `gitcom "Add commit message"`:

```bash
alias gitcom='function __gitcom(){ if [[ "${#1}" > 50 ]]; then echo "Commit message too long: ${#1} chars"; else git commit -m "$1"; fi }; __gitcom'
```

### commit etiquette
- try to keep commits small
- try not to commit changes that break code
- do not mix code changes e.g. changes in two unrelated functions or cleanup and functional change; makes it easier to document why which change has happened or identify when an issue has occurred.
- keep commit message subjects below 50 characters - makes the history easy to read and informative
- here is a good article about git [commit messages](https://chris.beams.io/posts/git-commit/)

### issue etiquette

- create issues on the upstream repository
- check if there already is an issue
- try to be as descriptive as possible 
- ideally add full code examples how an issue can be reproduced.
  example: https://github.com/G-Node/nixpy/issues/527
- if there is a related issue, refer to it: typing `#123` will automatically refer to issue 123
- for feature request issues make sure it is actually a single feature. If there are actually more features create more issues.

### pull request etiquette

- if possible keep the PRs reasonably small
- list all points that are addressed - if the commit description is through, use it
- refer to the issues it addresses - typing `#123` will automatically refer to issue 123
- you can also refer to other PRs via the running counter
- at first document if tests have passed with which version of a programming language and linters have been run until this becomes second nature before pushing in the first place.
- check back to pull requests whether all the tests and checks have succeeded.
- if there are issues, fix them and push the commits to the same branch; the PR will be updated automatically
- example: https://github.com/G-Node/python-odml/pull/389
