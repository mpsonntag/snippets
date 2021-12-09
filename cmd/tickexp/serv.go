package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/spf13/cobra"
)

// ExpItem holds information to describe ticket expenses
type ExpItem struct {
	Date   string  `json:"date"`
	Val    float64 `json:"val"`
	Negval float64 `json:"negval"`
	Desc   string  `json:"desc"`
}

func serv(cmd *cobra.Command, args []string) {
	fmt.Printf("Starting up %s", cmd.Version)

	// Start the HTTP handlers.

	// Root redirects to results
	http.Handle("/", http.RedirectHandler("/result", http.StatusMovedPermanently))

	// register renders the info page with the registration button
	http.HandleFunc("/result", func(w http.ResponseWriter, r *http.Request) {
		renderResultPage(w, r)
	})

	log.Fatal(http.ListenAndServe(":8899", nil))
}

func renderResultPage(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("Render results page")

	tmpl, err := template.New("Results").Parse(ResultsPage)
	if err != nil {
		fmt.Printf("Could not parse template: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	// read tickexp value file
	fp, err := os.Open("exp.json")
	if err != nil {
		fmt.Printf("Could not open value file: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	defer fp.Close()

	jdata, err := ioutil.ReadAll(fp)
	if err != nil {
		fmt.Printf("Could not read value file: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	var data []ExpItem
	if err = json.Unmarshal(jdata, &data); err != nil {
		fmt.Printf("Could not unmarshal value json data: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		fmt.Printf("Error rendering template: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}
