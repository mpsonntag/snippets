package main

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

var port = ":3030"
var outdir = filepath.Join(os.Getenv("HOME"), "Chaos", "DL")

func rootFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "It's alive!")
}

func uploadFormFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<html><body><form method='post' action='/uploaded'><input required type='text' name='content' id='content'><input type='submit' value='Submit'></form></body></html>")
}

func processUploadFunc(w http.ResponseWriter, r *http.Request) {
	var outfilepath = filepath.Join(outdir, "outfile.txt")

	content := r.FormValue("content")
	fmt.Fprintf(os.Stdout, "\n[Info] Received form value: %v\n", content)
	fmt.Fprintf(w, "<html><body><h1>Upload received</h1><a href='upload'>Upload more</a></body></html>")

	// sanitize input and split on comma
	contentslice := strings.Split(strings.ReplaceAll(content, " ", ""), ",")
	fmt.Fprintf(os.Stdout, "\n[Info] Sanitized, sliced content: '%v'\n\n", contentslice)

	// Write content to file
	outfile, err := os.OpenFile(outfilepath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n[Error] Could not open outfile for writing: '%v'\n\n", err)
		return
	}
	defer outfile.Close()
	for _, v := range contentslice {
		if v == "" {
			continue
		}
		fmt.Fprintf(os.Stdout, "\n[Info] Writing value '%s' to file", v)
		_, err = fmt.Fprintln(outfile, v)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\n[Error] Could not write content '%s' to file: '%v'\n\n", v, err)
		}
	}
}

func main() {
	if _, err := os.Stat(outdir); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "\n[Error] Output directory not found: '%v', abort...\n\n", outdir)
		os.Exit(-1)
	}

	http.HandleFunc("/", rootFunc)
	http.HandleFunc("/upload", uploadFormFunc)
	http.HandleFunc("/uploaded", processUploadFunc)
	server := http.Server{
		Addr: port,
	}

	fmt.Fprintln(os.Stdout, "[Start] Listen and serve")
	err := server.ListenAndServe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n[Error] Server startup: '%v', abort...\n\n", err)
		os.Exit(-1)
	}
}
