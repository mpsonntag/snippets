module github.com/mpsonntag/snippets/cmd/graphpush

go 1.16

require (
	github.com/G-Node/gin-cli v0.0.0-20200213155541-7b8a0596ebb3
	github.com/docopt/docopt-go v0.0.0-20180111231733-ee0de3bc6815
	github.com/felixge/httpsnoop v1.0.2 // indirect
	github.com/gorilla/handlers v1.5.1
	github.com/gorilla/mux v1.8.0
	github.com/spf13/cobra v1.3.0
)

replace github.com/docker/docker => github.com/docker/engine v1.13.1
