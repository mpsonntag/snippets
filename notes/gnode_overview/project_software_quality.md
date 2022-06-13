# Software quality tools

## go language tools

`go` tests and code quality tools

you can check out [the gin-doi](https://github.com/G-Node/gin-doi) how tests are set up and run; 
check out the github actions file (`.github/workflows/run-tests.yml`) to see how all formatting tools and tests
are executed.

Always run `go vet ./...`, `go fmt ./...` and `go test./...` before doing anything else. Ideally also use the other linters listed below.

I usually use the following snippet in my `.bash_alias` to run them as a custom `gohome` command before every commit / push to github to keep it convenient.

```bash
  alias gohome='function __gohome() { echo "RUN go lint"; golint ./... | grep -v vendor; echo "RUN go vet"; go vet ./...; echo "RUN gofmt"; go fmt ./...; echo "RUN go staticcheck"; staticcheck ./...; echo "RUN go errcheck"; errcheck ./... | grep -v defer; echo "RUN gocyclo"; gocyclo -over 15 .; echo "RUN go misspell"; find . -type f -name "*.go" | grep -v vendor/ | xargs misspell; echo "RUN go test"; go test -p 1 ./...; }; __gohome'
```

Linter and quality tools source and installation:

golint (deprecated, but for now still useful until fully replaced by other tools)
https://pkg.go.dev/golang.org/x/lint

staticcheck
https://github.com/dominikh/go-tools

errcheck
https://github.com/kisielk/errcheck

misspell
https://github.com/client9/misspell

gocyclo
https://github.com/fzipp/gocyclo


## Python tools

pylint
https://github.com/PyCQA/pylint

PEP8 in jupyter notebooks
https://stackoverflow.com/questions/26126853/verifying-pep8-in-ipython-notebook-code

```
pip install flake8 pycodestyle_magic
```

[... paraphrase]
- first load the magic in a Jupyter Notebook cell: `%load_ext pycodestyle_magic`
- and then turn on the magic to do compliance checking for each cell using: `%pycodestyle_on` or `%flake8_on`
- depending against which style guide you want to check. 
[...]
