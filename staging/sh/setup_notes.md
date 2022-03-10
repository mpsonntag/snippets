# Set software installation env variable
SOFTDIR=/home/$USER/Chaos/software

# Git state
function parse_git_branch {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/ [\1]/"
}
export PS1="\[\033[32m\]\u@\h \[\033[1;34m\]\w\[\033[0;33m\]\$(parse_git_branch)\[\033[00m\]$ "

# Add custom git shortcuts
alias gitmes='function __gitmes() { echo "Message length: ${#1} chars"; }; __gitmes'
alias gitcom='function __gitcom(){ if [[ "${#1}" > 50 ]]; then echo "Commit message too long: ${#1} chars"; else git commit -m "$1"; fi }; __gitcom'
alias gitlog='git log --oneline --graph'
alias gitag='git tag --list --format "%(align:width=30,position=left)%(color:magenta)%(refname:strip=2)%(color:reset)%(end)%(align:width=30,position=left)%(tag)%(end)%(subject)"'

# Custom alias'es
if [ -d "$SOFTDIR/pyvirtualenv" ]; then
  alias pyenv='source $SOFTDIR/pyvirtualenv/pymain/bin/activate'
  alias pyenv3='source $SOFTDIR/pyvirtualenv/py3main/bin/activate'
fi

# Add matlab to path
if [ -a "$SOFTDIR/Matlab/matlab" ]; then
  alias matdesk='sh $SOFTDIR/Matlab/matlab -desktop'
fi

# Add custom go shortcuts
if [ -d "$SOFTDIR/go" ]; then
  alias gocheck='function __gocheck() { echo "RUN go lint"; golint ./...; echo "RUN go vet"; go vet ./...; echo "RUN gofmt"; go fmt ./...; echo "RUN go mispell"; find . -type f -name "*.go" | grep -v vendor/ | xargs misspell;}; __gocheck'
  alias gohome='function __gohome() { echo "RUN go lint"; golint ./... | grep -v vendor; echo "RUN go vet"; go vet ./...; echo "RUN gofmt"; go fmt ./...; echo "RUN go staticcheck"; staticcheck ./...; echo "RUN go errcheck"; errcheck ./... | grep -v defer; echo "RUN gocyclo"; gocyclo -over 15 .; echo "RUN go mispell"; find . -type f -name "*.go" | grep -v vendor/ | xargs misspell; echo "RUN go test"; go test -p 1 ./...; }; __gohome'
  alias goclean='function __goclean() { go vet ./...; go fmt ./...; go test ./...; }; __goclean'
fi

# Add custom python linter shortcuts
alias pycheck='function __pycheck() { echo "RUN flake8"; flake8; }; __pycheck'

# alias conda='$HOME/Chaos/software/miniconda2/bin/conda'
alias condact='conda activate'
alias condeact='conda deactivate'

# Add docker cleanup alias
alias dockps='docker ps -aq --no-trunc -f status=exited | xargs docker rm'
alias dockim='docker images -f "dangling=true" -q | xargs docker rmi'
