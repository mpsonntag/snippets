package main

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
)

var port = ":3030"
var outdir = filepath.Join(os.Getenv("HOME"), "Chaos", "DL")
var outfilepath = filepath.Join(outdir, "outfile.txt")

func rootFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "It's alive!")
}

func uploadFormFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<html><body><form method='post' action='/uploaded'><input type='text' name='content' id='content'><input type='submit' value='Submit'></form></body></html>")
}

func processUploadFunc(w http.ResponseWriter, r *http.Request) {
	content := r.FormValue("content")
	fmt.Fprintf(os.Stdout, "\n[Info] received form value: %v", content)
	fmt.Fprintf(w, "<html><body><h1>Upload received</h1><a href='upload'>Upload more</a></body></html>")
}

func main() {
	if _, err := os.Stat(outdir); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "\n[Error] Output directory not found: '%v', abort...\n\n", outdir)
		os.Exit(-1)
	}

	if _, err := os.Stat(outfilepath); os.IsNotExist(err) {
		fmt.Fprint(os.Stdout, "\n[Start] Output file does not exist, creating.\n\n")
		outfile, err := os.Create(outfilepath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\n[Error] Could not create output file: '%v', abort ...\n\n", err)
			os.Exit(-1)
		}
		outfile.Close()
		fmt.Fprintf(os.Stdout, "\n[Start] Output file '%v' created.\n\n", outfilepath)
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
