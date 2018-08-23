package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/docopt/docopt-go"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"github.com/mpsonntag/snippets/cmd/graphpush/config"
	"github.com/G-Node/gin-valid/helpers"
	"github.com/G-Node/gin-valid/log"
)

const usage = `Server pushing rdf files to a defined fuseki server

Usage:
  graphpush [--listen=<port>] [--config=<path>]
  graphpush -h | --help
  graphpush --version

Options:
  -h --help           Show this screen.
  --version           Print version.
  --listen=<port>     Port to listen at [default:6066]
  --config=<path>     Path to a json server config file
  `

func postrdf(w http.ResponseWriter, r *http.Request) {
	srvcfg := config.Read()

	fname := "/home/msonntag/Chaos/DL/odmlconvdir/odmlconv_zvutnp2y/odmlrdf_7wgd4x30/2_conv.rdf"
	content, err := ioutil.ReadFile(fname)
	if err != nil {
		log.ShowWrite("[Error] reading RDF file\n")
		os.Exit(-1)
	}

	client := &http.Client{}

	request, _ := http.NewRequest("POST", "http://meta.g-node.org:3030/odml-gen/data", bytes.NewReader(content))
	request.SetBasicAuth(srvcfg.Settings.MetaUser, srvcfg.Settings.MetaPW)
	request.Header.Add("Content-Type", "application/rdf+xml")

	resp, err := client.Do(request)
	if err != nil {
		log.ShowWrite("[Error] posting RDF file: %v\n", err.Error())
		os.Exit(-1)
	}

	log.ShowWrite("[Info] RDF file post status: '%s', \n", resp.Status)
}

func root(w http.ResponseWriter, r *http.Request) {
	http.ServeContent(w, r, "root", time.Now(), bytes.NewReader([]byte("alive")))
}

func registerRoutes(r *mux.Router) {
	r.HandleFunc("/", root)
	r.HandleFunc("/rdfupload", postrdf)
}

func main() {

	// Initialize and read the default server config
	srvcfg := config.Read()

	// Parse commandline arguments
	args, err := docopt.ParseArgs(usage, nil, "v1.0.0")
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n[Error] parsing cli arguments: '%s', abort...\n\n", err.Error())
		os.Exit(-1)
	}

	// Parse and load custom server confguration
	if args["--config"] != nil {
		content, err := ioutil.ReadFile(args["--config"].(string))
		if err != nil {
			fmt.Fprintf(os.Stderr, "[Error] reading config file %v\n", args["--config"])
			os.Exit(-1)
		}

		// Overwrite any default settings with information from the
		// provided config file.
		err = json.Unmarshal(content, &srvcfg)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[Error] unmarshalling config file %s\n", err.Error())
			os.Exit(-1)
		}
		config.Set(srvcfg)
	}

	err = log.Init()
	if err != nil {
		fmt.Fprintf(os.Stderr, "[Error] opening logfile '%s'\n", err.Error())
		os.Exit(-1)
	}
	defer log.Close()

	// Log cli arguments
	log.Write("[Warmup] cli arguments: %v\n", args)

	// Check whether the required directories are available and accessible
	if !helpers.ValidDirectory(srvcfg.Dir.Source) {
		os.Exit(-1)
	}

	log.ShowWrite("[Warmup] using source directory: '%s'\n", srvcfg.Dir.Source)

	// Use port if provided.
	var port string
	if argport := args["--listen"]; argport != nil {
		port = argport.(string)
	}

	if helpers.IsValidPort(port) {
		port = fmt.Sprintf(":%s", port)
	} else {
		port = fmt.Sprintf(":%s", srvcfg.Settings.Port)
		log.ShowWrite("[Warning] could not parse a valid port number, using default\n")
	}
	log.ShowWrite("[Warmup] using port: '%s'\n", port)

	log.ShowWrite("[Warmup] registering routes\n")
	router := mux.NewRouter()
	registerRoutes(router)

	handler := handlers.CORS(
		handlers.AllowedHeaders([]string{"Accept", "Content-Type", "Authorization"}),
		handlers.AllowedOrigins([]string{"*"}),
		handlers.AllowedMethods([]string{"GET"}),
	)(router)

	server := http.Server{
		Addr:    port,
		Handler: handler,
	}

	// Monitor the environment for shutdown signals to
	// gracefully shutdown the server.
	go func() {
		sigchan := make(chan os.Signal, 1)
		signal.Notify(sigchan, os.Interrupt)
		<-sigchan
		log.ShowWrite("[Info] System interrupt, shutting down server\n")
		err := server.Shutdown(context.Background())
		if err != nil {
			log.ShowWrite("[Error] on server shutdown: %v\n", err)
		}
	}()

	log.ShowWrite("[Start] Listen and serve\n")
	err = server.ListenAndServe()
	if err == http.ErrServerClosed {
		log.Close()
		os.Exit(0)
	} else if err != nil {
		log.ShowWrite("[Error] Server startup: '%v', abort...\n\n", err)
		log.Close()
		os.Exit(-1)
	}
}
