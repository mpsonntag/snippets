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
	"strings"
	"time"

	"github.com/G-Node/gin-valid/helpers"
	"github.com/docopt/docopt-go"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"github.com/mpsonntag/snippets/cmd/graphpush/config"
	"github.com/mpsonntag/snippets/cmd/graphpush/log"
)

const usage = `Server pushing RDF files to a specific fuseki server graph

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

	request, _ := http.NewRequest("POST", srvcfg.Settings.FusekiURI, bytes.NewReader(content))
	request.SetBasicAuth(srvcfg.Settings.MetaUser, srvcfg.Settings.MetaPW)
	request.Header.Add("Content-Type", "application/rdf+xml")

	resp, err := client.Do(request)
	if err != nil {
		log.ShowWrite("[Error] posting RDF file: %v", err.Error())
		os.Exit(-1)
	}

	log.ShowWrite("[Info] RDF file post status: '%s'", resp.Status)
}

func convertup(w http.ResponseWriter, r *http.Request) {
	// Initialize and read the default server config
	srvcfg := config.Read()

	vars := mux.Vars(r)
	graph := vars["graph"]
	log.ShowWrite("[Info] handling conversion and upload to graph '%s'", graph)

	log.ShowWrite("[Info] making sure server is there and alive")
	client := &http.Client{}
	request, _ := http.NewRequest("GET", fmt.Sprintf("%s/$/ping", srvcfg.Settings.FusekiURI), nil)
	resp, err := client.Do(request)
	if err != nil {
		log.ShowWrite("[Error] pinging Fuseki: '%s'", err.Error())
		return
	}
	log.ShowWrite("[Info] Fuseki ping response: '%s'", resp.Status)
}

func root(w http.ResponseWriter, r *http.Request) {
	http.ServeContent(w, r, "root", time.Now(), bytes.NewReader([]byte("alive")))
}

func registerRoutes(r *mux.Router) {
	r.HandleFunc("/", root)
	r.HandleFunc("/fileup", postrdf)
	r.HandleFunc("/convertup/{graph}", convertup)
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

	// Parse and load custom server configuration
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

	err = log.Init(srvcfg.Dir.Log, srvcfg.Settings.LogFile, srvcfg.Settings.LogSize)
	if err != nil {
		fmt.Fprintf(os.Stderr, "[Error] opening logfile '%s'\n", err.Error())
		os.Exit(-1)
	}
	defer log.Close()

	// Log cli arguments
	log.Write("[Warmup] cli arguments: %v", args)

	// Check whether the required directories are available and accessible
	if !helpers.ValidDirectory(srvcfg.Dir.Source) {
		os.Exit(-1)
	}
	log.ShowWrite("[Warmup] using source directory: '%s'", srvcfg.Dir.Source)

	// Check that the odmltordf script is available
	outstr, err := helpers.AppVersionCheck("odmltordf")
	if err != nil {
		log.ShowWrite("[Error] checking odmltordf '%s'", err.Error())
		os.Exit(-1)
	}
	log.ShowWrite("[Warmup] using odmltordf v%s", strings.TrimSpace(outstr))

	// Use port if provided.
	var port string
	if argport := args["--listen"]; argport != nil {
		port = argport.(string)
	}

	if helpers.IsValidPort(port) {
		port = fmt.Sprintf(":%s", port)
	} else {
		port = fmt.Sprintf(":%s", srvcfg.Settings.Port)
		log.ShowWrite("[Warning] could not parse a valid port number, using default")
	}
	log.ShowWrite("[Warmup] using port: '%s'", port)

	log.ShowWrite("[Warmup] registering routes")
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
			log.ShowWrite("[Error] on server shutdown: '%v'", err)
		}
	}()

	log.ShowWrite("[Start] Listen and serve")
	err = server.ListenAndServe()
	if err == http.ErrServerClosed {
		log.Close()
		os.Exit(0)
	} else if err != nil {
		log.ShowWrite("[Error] Server startup: '%v', abort...\n", err)
		log.Close()
		os.Exit(-1)
	}
}
