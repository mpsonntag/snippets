# Git annex notes

All infos distilled from https://git-annex.branchable.com

## Key concept
Annexing a file does three things:
- it moves the content of the file into a key value store.
- it creates a symlink that points to the content in the key-value store.
- it replaces the file with a placeholder that contains the symlink location and checks this file into git.

When such a repo now is pushed, the file containing the symlink is pushed, but the content is not and has to be uploaded to another remote specifically.

## File location
The content of large files can be found in the `.git/annex` directory; the annex pointer files checked into git will point to these locations.

To avoid having too many files in a single folder, the first 6 characters of the md5 sum of the file key are used to create two levels of folders e.g. `.git/annex/f87/4d5/`

git annex keeps track which remotes contain the actual content of a file. On a content get, it will either fetch the content from any available remote that has the content or print which remote might have the content, that is currently unavailable. [???] This information is probably obtained and recorded whenever a git annex sync takes place, but still unclear where exactly this information is stored; in the file placeholder?

## Automatic conflict resolution
When two or more files have diverged, upon a merge, they will be renamed to `filename.variant-AAA`, `filename.variant-BBB`, etc; its up to the user to resolve the conflict at this point.

## Annex sync
- `git annex sync` ... updates all connected repositories on all available distributed hosts
- the branch `synced/master` is used to this end.

The workflow is as follows when `git annex sync` is run
- merge local `synced/master` into local `master`
- conflicts are resolved by 'automatic conflict resolution'.
- fetch each remote successively and merge changes from there.
- update local `sync/master` with the local state.
- push `sync/master` to all defined remotes.

Note that only `git annex sync --content` also transfers the actual content to other repos, by default only placeholder files are synced.
Note that when the history of the git master branch is changed e.g. by dropping a commit, the `synced/master` branch will recreate this commit before an upload.
