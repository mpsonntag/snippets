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
GINSERVERALIAS=dev

cd $REPOPATH
REPO=$(basename "$PWD")

echo "Download git changes from origin"
gin download

echo "Download annex changes from origin"
gin get-content .

echo "Add DOI fork as remote"
gin add-remote doi $GINSERVERALIAS:doi/$REPO

echo "Upload to DOI fork"
gin upload --to=doi

echo "Done!"
