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
