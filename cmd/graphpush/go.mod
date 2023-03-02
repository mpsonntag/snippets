module github.com/mpsonntag/snippets/cmd/graphpush

go 1.20

require (
	github.com/docopt/docopt-go v0.0.0-20180111231733-ee0de3bc6815
	github.com/gorilla/handlers v1.5.1
	github.com/gorilla/mux v1.8.0
)

require github.com/felixge/httpsnoop v1.0.2 // indirect

replace github.com/docker/docker => github.com/docker/engine v1.13.1
