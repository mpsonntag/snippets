# Git annex notes

All infos distilled from https://git-annex.branchable.com

## File location

## File location
The content of large files can be found in the `.git/annex` directory; the annex pointer files checked into git will point to these locations.

To avoid having too many files in a single folder, the first 6 characters of the md5 sum of the file key are used to create two levels of folders e.g. `.git/annex/f87/4d5/`

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
