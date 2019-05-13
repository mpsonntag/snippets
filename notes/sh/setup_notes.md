# Set software installation env variable
SOFTDIR=/home/username/Chaos/software

# Git state
function parse_git_dirty {
  [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
}

function parse_git_branch {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/[\1$(parse_git_dirty)]/"
}
export PS1='\u@\h \[\033[1;33m\]\w\[\033[0m\]$(parse_git_branch)$ '

# Add custom git shortcuts
alias gitmes='function __gitmes() { echo "Message length: ${#1} chars"; }; __gitmes'
alias gitcom='function __gitcom(){ if [[ "${#1}" > 50 ]]; then echo "Commit message too long: ${#1} chars"; else git commit -m "$1"; fi }; __gitcom'
alias gitlog='git log --oneline --graph'

# Custom alias'es
if [ -d $SOFTDIR"/pyvirtualenv" ]; then
  alias pyenv='source $SOFTDIR/pyvirtualenv/pymain/bin/activate'
  alias pyenv3='source $SOFTDIR/pyvirtualenv/py3main/bin/activate'
  alias pydl='source $SOFTDIR/pyvirtualenv/pydl/bin/activate'
fi

# Add matlab to path
if [ -e $SOFTDIR"/Matlab/matlab" ]; then
  alias matdesk='sh $SOFTDIR/Matlab/matlab -desktop'
fi

# Add custom go shortcuts
if [ -d $SOFTDIR"/go" ]; then
  alias gocheck='function __gocheck() { echo "RUN gocyclo"; gocyclo -over 15 .; echo "RUN go lint"; fgt golint -min_confidence 0.9 ./...; echo "RUN go vet"; go vet ./...; echo "RUN gofmt"; gofmt -l .; echo "RUN go ineffassign"; ineffassign .; echo "RUN gosimple"; gosimple ./...; }; __gocheck'
  alias gohome='function __gohome() { echo "RUN go lint"; fgt golint -min_confidence 0.9 ./...; echo "RUN go vet"; go vet ./...; echo "RUN gofmt"; gofmt -l -w .; echo "RUN go ineffassign"; ineffassign .; echo "RUN gosimple"; gosimple ./...; echo "RUN go staticcheck"; staticcheck ./...; echo "RUN go errcheck"; errcheck ./...; echo "RUN go test"; go test -p 1 ./...; }; __gohome'
fi

# Add custom python linter shortcuts
alias pycheck='function __pycheck() { echo "RUN flake8"; flake8; }; __pycheck'

# alias conda=$SOFTDIR'/miniconda2/bin/conda'
alias condact='conda activate'
alias condeact='conda deactivate'

# Add docker cleanup alias
alias dockps='docker ps -aq --no-trunc -f status=exited | xargs docker rm'
alias dockim='docker images -f "dangling=true" -q | xargs docker rmi'
