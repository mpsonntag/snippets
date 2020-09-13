package main

import (
	"fmt"
	"net/http"
	"os"
)

func rootFunc(w http.ResponseWriter, r *http.Request){
	fmt.Fprintf(w, "It's alive!")
}

func main() {
	http.HandleFunc("/", rootFunc)
	server := http.Server{
		Addr: ":3030",
	}

	fmt.Fprintln(os.Stdout, "[Start] Listen and serve")
	err := server.ListenAndServe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n[Error] Server startup: '%v', abort...\n\n", err)
		os.Exit(-1)
	}
}
