## Creating and deploying a new release of GCA-Web

- add a new release directly before a new release is actually deployed on the live server `abstracts.g-node.org`.
- document all changes since the last version in the CHANGELOG.md file of the GCA-Web repository.
- build a docker version with the release version of the code. give it the same name as the release tag will have. e.g. `gnode/gca:v1.3`. push this version to dockerhub.
- deploy this version from dockerhub on the dev server and test thoroughly
- update code, CHANGELOG and docker image if necessary.
- when everything works, create a git tag with the appropriate version number.
- push to github and create a release
- deploy exactly that version on the live server.
