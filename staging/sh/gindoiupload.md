#!/usr/bin/env bash
#
# Downloads potential changes into an existing gin repository
# and uploads the repository to an existing gin fork of the gin "doi" user.

if [[ $# < 1 ]]; then
  echo "Need a path to an downloaded repository"
  exit 1
fi

if ! gin info | grep -iq "user doi"; then
  echo "Please log in to GIN as the DOI user (with the gin client)"
  exit 1
fi

REPOPATH=$1

cd $REPOPATH
REPO=$(basename "$PWD")

echo "Done!"
