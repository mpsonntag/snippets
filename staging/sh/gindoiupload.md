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
WORKIR=$PWD
REPO=$(basename "$PWD")

cd ..
TAGNAME=10.12751/$(basename "$PWD")
echo "... using tag name $TAGNAME"

cd  $WORKDIR
echo "... working in directory $PWD"

echo "... checking doi fork"
if ! gin repoinfo doi/$REPO | grep -iq "[error]"; then
  echo "... could not find fork doi/$REPO"
  exit 1
fi

echo "... download git changes from origin"
gin download

echo "... download annex changes from origin"
gin get-content .

echo "... add DOI fork as remote"
gin add-remote doi $GINSERVERALIAS:doi/$REPO

echo "... switch remote and upload file content to DOI fork"
gin use-remote doi
gin upload .

echo "... create and upload DOI tag"
gin git tag $TAGNAME
gin git push --tags doi

echo "... Done!"
