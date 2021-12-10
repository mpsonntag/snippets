package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/spf13/cobra"
)

const datastorage = "exp.json"
const baseval = "949"

// ExpItem holds information to describe ticket expenses
type ExpItem struct {
	Date   string  `json:"date"`
	Val    float64 `json:"val"`
	Negval float64 `json:"negval"`
	Desc   string  `json:"desc"`
}

// fileSetUp creates an empty data storage json file if it does not yet exist
func fileSetUp() error {
	fmt.Println("...[I] setting up data file")
	_, err := os.Stat(datastorage)
	if err == nil {
		return nil
	} else if os.IsNotExist(err) {
		var jstring []string
		jdata, err := json.Marshal(jstring)
		if err != nil {
			return err
		}
		err = ioutil.WriteFile(datastorage, jdata, 0644)
		return err
	}

	// return any error other than os.IsNotExist as is
	return err
}

// serv checks and sets up datastorage file, registers available routes
// and starts the server
func serv(cmd *cobra.Command, args []string) {
	fmt.Printf("...[I] starting serv (%s)\n", cmd.Version)

	err := fileSetUp()
	if err != nil {
		fmt.Printf("...[E] setting up data file: %s\n", err.Error())
		fmt.Printf("...[E] abort\n")
		os.Exit(-1)
	}

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

	// raw provides the datastorage file content
	http.HandleFunc("/raw", func(w http.ResponseWriter, r *http.Request) {
		serveDataFile(w, r)
	})

	log.Fatal(http.ListenAndServe(":8899", nil))
}

// serveDataFile provides the raw datastorage file content
func serveDataFile(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] serving file content")
	http.ServeFile(w, r, datastorage)
}

// dataAdd parses form value from a POST and adds to the data storage file
func dataAdd(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] handling form data")

	if r.Method != "POST" {
		fmt.Printf("...[E] receiving invalid request: '%s'\n", r.Method)
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}
	if err := r.ParseForm(); err != nil {
		fmt.Printf("...[E] parsing form request: '%s'\n", err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}

	date := r.FormValue("date")
	val := r.FormValue("val")
	desc := r.FormValue("desc")
	fmt.Printf("...[I] receiving form values: '%s, %s, %s'\n", date, val, desc)

	// data checks and cleanup
	var negval float64
	val = strings.TrimSpace(val)
	if strings.Contains(val, "-") {
		splitval := strings.Split(val, "-")
		val = strings.TrimSpace(splitval[0])

		// handle additional negative value
		strnegval := strings.TrimSpace(splitval[1])
		stuff, err := strconv.ParseFloat(strnegval, 64)
		if err != nil {
			fmt.Printf("...[E] converting negval '%s' to float: %s\n", strnegval, err.Error())
			http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
			return
		}
		negval = stuff
	}

	floatval, err := strconv.ParseFloat(val, 64)
	if err != nil {
		fmt.Printf("...[E] converting value '%s' to float: %s\n", val, err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}

	curr := ExpItem{
		Date:   date,
		Val:    floatval,
		Negval: negval,
		Desc:   desc,
	}

	var indata []ExpItem
	data, err := readDataFile(indata)
	if err != nil {
		fmt.Printf("...[E] reading json data storage file: '%s'\n", err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}
	data = append(data, curr)
	jdata, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		fmt.Printf("...[E] marshalling json data: %s\n", err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}
	err = ioutil.WriteFile(datastorage, jdata, 0644)
	if err != nil {
		fmt.Printf("...[E] writing new data to data storage: %s\n", err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}

	http.Redirect(w, r, "/add", http.StatusSeeOther)
}

func renderAddPage(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("...[I] rendering AddPage\n")

	// read tickexp value file
	var data []ExpItem
	data, err := readDataFile(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("Add").Parse(AddPage)
	if err != nil {
		fmt.Printf("...[E] parsing AddPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		fmt.Printf("...[E] rendering AddPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

// readDataFile reads data from the dedicated json file and returns
// the unmarshalled json data
func readDataFile(data []ExpItem) ([]ExpItem, error) {
	fp, err := os.Open("exp.json")
	if err != nil {
		return nil, fmt.Errorf("...[E] opening data storage file: %s", err.Error())
	}

	fileclose := func(fp *os.File) {
		err := fp.Close()
		if err != nil {
			fmt.Printf("...[E] closing data file: %s", err.Error())
		}
	}
	defer fileclose(fp)

	jdata, err := ioutil.ReadAll(fp)
	if err != nil {
		return nil, fmt.Errorf("...[E] reading data storage file: %s", err.Error())
	}

	if err = json.Unmarshal(jdata, &data); err != nil {
		return nil, fmt.Errorf("...[E] unmarshalling json data: %s", err.Error())
	}
	return data, nil
}

// DisplayResults is the struct handed to the frontend to display all relevant information
type DisplayResults struct {
	Data      []ExpItem
	Valsum    float64
	Negvalsum float64
	Offsetval float64
}

var tmplfuncs = template.FuncMap{
	"legrande": Legrande,
	"ppfloat":  ppfloat,
}

// ppfloat returns a float value as formatted string
func ppfloat(val float64) string {
	return fmt.Sprintf("%.2f", val)
}

// Legrande takes a base float, adds and substracts the respective provided values
// and returns the result as a formatted string
func Legrande(base, pos, neg float64) string {
	return fmt.Sprintf("%.2f", base+pos-neg)
}

func renderResultPage(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("...[I] rendering ResultPage\n")

	// read tickexp value file
	var data []ExpItem
	data, err := readDataFile(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	frontdata, err := constructResultsData(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("Results").Funcs(tmplfuncs).Parse(ResultsPage)
	if err != nil {
		fmt.Printf("...[E] parsing ResultPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, frontdata)
	if err != nil {
		fmt.Printf("...[E] rendering ResultPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

func constructResultsData(data []ExpItem) (*DisplayResults, error) {
	// handle offsetvalue - might change on runtime so always convert from string to float64
	offval, err := strconv.ParseFloat(baseval, 64)
	if err != nil {
		return nil, fmt.Errorf("...[E] parsing the base offset value: %s", err.Error())
	}

	// get the grand total
	valsum, negvalsum := calcresult(data)

	frontdata := DisplayResults{
		Data:      data,
		Valsum:    valsum,
		Negvalsum: negvalsum,
		Offsetval: offval,
	}
	return &frontdata, nil
}

func calcresult(data []ExpItem) (float64, float64) {
	var valsum float64
	var negvalsum float64
	for _, item := range data {
		valsum += item.Val
		negvalsum += item.Negval
	}
	return valsum, negvalsum
}
