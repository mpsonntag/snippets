# Git annex notes


## Annex sync
`git annex sync` ... updates all connected repositories

The branch `synced/master` is used to this end.

The workflow is as follows when sync is run
- merge `synced/master` into local `master`
- conflicts are resolved by 'automatic conflict resolution'.
- fetch each remote successively and merge changes from there.
- update `sync/master` with the local state
- push `sync/master` to all remotes

Note that only `git annex sync --content` also transfers the actual content to other repos, by default only placeholder files are synced.
