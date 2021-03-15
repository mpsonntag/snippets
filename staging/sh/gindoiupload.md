#!/usr/bin/env bash
#
# Downloads potential changes from the default server into an existing gin repository
# and uploads the repository to an existing gin fork of the gin "doi" user.

# server alias for uploads; should be 'gin'
GINSERVERALIAS=dev

if [[ $# < 1 ]]; then
  echo "... need a path to a downloaded gin repository"
  exit 1
fi

REPOPATH=$1
if [ ! -d $REPOPATH ]; then
    echo "... $REPOPATH is not a valid directory"
    echo "    exiting..."
    exit 1
fi

echo "... checking gin client user"
if ! gin info | grep -iq "user doi"; then
  echo "... please log in to GIN as the DOI user (with the gin client)"
  exit 1
fi

cd $REPOPATH
REPO=$(basename "$PWD")
echo "... working in directory $PWD"

echo "... download git changes from origin"
gin download

echo "... download annex changes from origin"
gin get-content .

echo "... add DOI fork as remote"
gin add-remote doi $GINSERVERALIAS:doi/$REPO

echo "... upload file content to DOI fork"
gin upload --to=doi

echo "... Done!"
