#!/usr/bin/env bash
#
# Downloads potential changes from the default server into an existing gin repository
# and uploads the repository to an existing gin fork of the gin "doi" user.

# server alias for uploads; should be 'gin'
GINSERVERALIAS=dev

echo "... working with gin server '$GINSERVERALIAS'"

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
WORKDIR=$PWD
REPO=$(basename "$PWD")
if [[ $# > 1 ]]; then
  REPO=$2
  echo "... using alternative DOI repository at $REPO"
fi

cd ..
TAGNAME=10.12751/$(basename "$PWD")
echo "... using tag name $TAGNAME"

cd $WORKDIR
echo "... working in directory $PWD"

echo "... checking doi fork"
if ! gin repoinfo doi/$REPO | grep -iq "[error]"; then
  echo "... could not find fork doi/$REPO"
  exit 1
fi

ZIPCOMMIT=$(git log -1 --pretty=oneline | cut -d' ' -f1)

echo "... download git changes from origin"
gin download

echo "... download annex changes from origin"
gin get-content .

DLCOMMIT=$(git log -1 --pretty=oneline | cut -d' ' -f1)
echo "... checking repository state"
if [[ $ZIPCOMMIT = $DLCOMMIT ]]; then
  echo "... repo is at the DOI request state; commits are identical"
  REPODIFF="... repo was at the DOI request state; last commits were identical"
else
  echo "... repo is not at the DOI request state; expected commit: $ZIPCOMMIT; found commit: $DLCOMMIT"
  REPODIFF="... repo was not at the DOI request state; expected commit: $ZIPCOMMIT; found commit: $DLCOMMIT"
fi

echo "... add DOI fork as remote"
gin add-remote doi $GINSERVERALIAS:doi/$REPO

echo "... switch remote and upload file content to DOI fork"
gin use-remote doi
gin upload .

echo "... create and upload DOI tag"
gin git tag $TAGNAME
gin git push --tags doi

echo $REPODIFF
echo "... Done!"
