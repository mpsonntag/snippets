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

	// root redirects to results
	http.Handle("/", http.RedirectHandler("/result", http.StatusMovedPermanently))

	// result renders the total sum and full data list
	http.HandleFunc("/result", func(w http.ResponseWriter, r *http.Request) {
		renderResultPage(w, r)
	})

	// add provides the data entry form
	http.HandleFunc("/add", func(w http.ResponseWriter, r *http.Request) {
		renderAddPage(w, r)
	})

	// dataadd adds form entry to the data file
	http.HandleFunc("/dataadd", func(w http.ResponseWriter, r *http.Request) {
		dataAdd(w, r)
	})

	log.Fatal(http.ListenAndServe(":8899", nil))
}

func dataAdd(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("... handle form data\n")

	if r.Method != "POST" {
		fmt.Printf("received invalid request '%s'\n", r.Method)
		return
	}
	if err := r.ParseForm(); err != nil {
		fmt.Printf("error parsing form request: '%s'\n", err.Error())
		return
	}

	date := r.FormValue("date")
	val := r.FormValue("val")
	desc := r.FormValue("desc")

	fmt.Printf("received form values: '%s, %s, %s'\n", date, val, desc)
}

func renderAddPage(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("... render 'Add' page\n")

	tmpl, err := template.New("Add").Parse(AddPage)
	if err != nil {
		fmt.Printf("could not parse 'Add' template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, nil)
	if err != nil {
		fmt.Printf("error rendering 'Add' template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

// readDataFile reads data from the dedicated json file and returns
// the unmarshalled json data
func readDataFile(data []ExpItem) ([]ExpItem, error) {
	fp, err := os.Open("exp.json")
	if err != nil {
		return nil, fmt.Errorf("could not open value file: %s", err.Error())
	}

	defer fp.Close()

	jdata, err := ioutil.ReadAll(fp)
	if err != nil {
		return nil, fmt.Errorf("could not read value file: %s", err.Error())
	}

	if err = json.Unmarshal(jdata, &data); err != nil {
		return nil, fmt.Errorf("could not unmarshal value json data: %s", err.Error())
	}
	return data, nil
}

func renderResultPage(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("... render results page\n")

	var data []ExpItem
	// read tickexp value file
	data, err := readDataFile(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("Results").Parse(ResultsPage)
	if err != nil {
		fmt.Printf("could not parse template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		fmt.Printf("error rendering template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}
