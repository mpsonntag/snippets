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

