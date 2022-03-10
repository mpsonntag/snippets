package main

import (
	"crypto/rand"
	"encoding/base32"
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

const defaultPort = ":8899"

// datastorage specifies the data storage file location and file name
const datastorage = "exp.json"

const cookieName = "tickexp-bearer-token"

// baseval is the base value on which all calculations are based on
const baseval = "949"

// regexpdate is the regular expression checking the date input in frontend and backend
// dates in the format 'DD.MM.YYYY' in the year range 1900-2099 are supported
const regexpdate = "(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).(19[0-9]{2}|20[0-9]{2})"

// regexpval is the regular expression checking the value input in frontend and backend
// two float values with two after digits separated by a minus are supported
const regexpval = `[0-9]+([\.][0-9]{0,2})?(-[0-9]+([\.][0-9]{0,2})?)*`

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
		fmt.Println("...[E] abort")
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

	// loginpage provides what it says
	http.HandleFunc("/loginpage", func(w http.ResponseWriter, r *http.Request) {
		renderLoginPage(w, r)
	})

	// login handles login to the service
	http.HandleFunc("/login", func(w http.ResponseWriter, r *http.Request) {
		handleLogin(w, r)
	})

	useport := defaultPort
	fmt.Printf("...[I] running server on port %s\n", useport)
	log.Fatal(http.ListenAndServe(useport, nil))
}

// renderLoginPage provides the page to log in
func renderLoginPage(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] rendering login page")

	tmpl, err := template.New("Login").Funcs(tmplfuncs).Parse(LoginPage)
	if err != nil {
		fmt.Printf("...[E] parsing LoginPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	data := struct {
		ReferenceVal string
	}{
		ReferenceVal: "somestring",
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		fmt.Printf("...[E] rendering LoginPage template: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

// handleLogin parses login data
func handleLogin(w http.ResponseWriter, r *http.Request) {
	checkphrase := "iam"
	checkpass := "soami"
	checkhidden := "somestring"

	fmt.Println("...[I] handling login data")
	fmt.Printf("...[I] logging request: {%s, %s, %s}\n", r.Method, r.URL, r.UserAgent())

	// map user agent against hidden+timestamp and only allow login attempts where
	// hidden+timestamp and user agent fingerprint aligns

	if r.Method != "POST" {
		fmt.Printf("...[E] receiving invalid login request: '%s'\n", r.Method)
		http.Redirect(w, r, "/loginpage", http.StatusTemporaryRedirect)
		return
	}
	if err := r.ParseForm(); err != nil {
		fmt.Printf("...[E] parsing login form request: '%s'\n", err.Error())
		http.Redirect(w, r, "/loginpage", http.StatusTemporaryRedirect)
		return
	}

	formphrase := r.FormValue("phrase")
	formpass := r.FormValue("pass")
	formref := r.FormValue("reference")
	fmt.Printf("...[I] receiving form values: '%s, %s, %s'\n", formphrase, formpass, formref)

	if formphrase != checkphrase || formpass != checkpass || checkhidden != formref {
		fmt.Println("...[E] invalid login")
		http.Redirect(w, r, "/loginpage", http.StatusTemporaryRedirect)
		return
	}

	// set cookie
	fmt.Printf("...[I] login successful; creating cookie")
	currCookieVal := RandomToken()
	cookieExpiration := time.Now().Add(1 * time.Minute)

	newc := http.Cookie{
		Name:     cookieName,
		Value:    currCookieVal,
		HttpOnly: true,
		Expires:  cookieExpiration,
	}
	http.SetCookie(w, &newc)

	http.Redirect(w, r, "/results", http.StatusTemporaryRedirect)
}

// serveDataFile provides the raw datastorage file content
func serveDataFile(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] serving file content")
	fmt.Printf("...[I] logging request: {%s, %s}\n", r.Method, r.URL)

	http.ServeFile(w, r, datastorage)
}

// safeguardInput takes date and value form inputs, checks against
// the appropriate regular expressions and returns an error if required.
func safeguardInput(date, val string) error {
	ok, err := regexp.MatchString(regexpdate, date)
	if err != nil {
		return fmt.Errorf("...[E] parsing date regexp: %s", err.Error())
	} else if !ok {
		return fmt.Errorf("...[W] invalid date received: %s", date)
	}
	ok, err = regexp.MatchString(regexpval, val)
	if err != nil {
		return fmt.Errorf("...[E] parsing value regexp: %s", err.Error())
	} else if !ok {
		return fmt.Errorf("...[W] invalid value received: %s", val)
	}
	return nil
}

// dataAdd parses form value from a POST and adds to the data storage file
func dataAdd(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] handling form data")
	fmt.Printf("...[I] logging request: {%s, %s}\n", r.Method, r.URL)

	// check if cookie is valid and redirect if it is not
	handleCookie(w, r)

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

	// safeguard input data
	fmt.Println("...[I] checking form values")
	err := safeguardInput(date, val)
	if err != nil {
		fmt.Println(err.Error())
		http.Redirect(w, r, "/add", http.StatusTemporaryRedirect)
		return
	}

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

// handleCookie checks whether the server named cookie is present.
// If not, redirect to the login page.
func handleCookie(w http.ResponseWriter, r *http.Request) {
	// implement cookie value check; requires server side cookie value and
	// expiration time storage and mapping. Expiration time is not provided
	// via the request cookie - only name and value.
	_, err := r.Cookie(cookieName)
	if err != nil {
		fmt.Printf("...[E] fetching cookie: %s\n", err.Error())
		http.Redirect(w, r, "/loginpage", http.StatusTemporaryRedirect)
		return
	}
}

// renderAddPage renders the data input page
func renderAddPage(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] rendering AddPage")
	fmt.Printf("...[I] logging request: {%s, %s}\n", r.Method, r.URL)

	// check if cookie is valid and redirect if it is not
	handleCookie(w, r)

	// read tickexp value file
	var data []ExpItem
	data, err := readDataFile(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	tmpl, err := template.New("Add").Funcs(tmplfuncs).Parse(AddPage)
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
			fmt.Printf("...[E] closing data file: %s\n", err.Error())
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

// tmplfuncs maps the functions usable in the frontend templates
var tmplfuncs = template.FuncMap{
	"legrande":   legrande,
	"ppfloat":    ppfloat,
	"currdate":   currdate,
	"regexpdate": serveregexpdate,
	"regexpval":  serveregexpval,
}

// serveregexpdate provides the date regular expression for the frontend template
func serveregexpdate() string {
	return regexpdate
}

// serveregexpval provides the value regular expression for the frontend template
func serveregexpval() string {
	return regexpval
}

// currdate returns the current date formatted as date "DD.MM.YYYY"
func currdate() string {
	notapres := time.Now()
	return notapres.Format("02.01.2006")
}

// ppfloat returns a float value as formatted string
func ppfloat(val float64) string {
	return fmt.Sprintf("%.2f", val)
}

// legrande takes a base float, adds and subtracts the respective provided values
// and returns the result as a formatted string
func legrande(base, pos, neg float64) string {
	return fmt.Sprintf("%.2f", base+pos-neg)
}

// renderResultPage renders the calculations results page
func renderResultPage(w http.ResponseWriter, r *http.Request) {
	fmt.Println("...[I] rendering ResultPage")
	fmt.Printf("...[I] logging request: {%s, %s}\n", r.Method, r.URL)

	// read tickexp value file
	var data []ExpItem
	data, err := readDataFile(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	// create the frontend data object
	frontdata, err := constructResultsData(data)
	if err != nil {
		fmt.Println(err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	// prepare the required templates
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

// constructResultsData takes an array of ExpItems, creates the positive and negative sum
// value totals from the data items and creates and returns the frontend data object
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

// calcresult sums up the positive and negative values from a []ExpItem and
// returns the resulting values
func calcresult(data []ExpItem) (float64, float64) {
	var valsum float64
	var negvalsum float64
	for _, item := range data {
		valsum += item.Val
		negvalsum += item.Negval
	}
	return valsum, negvalsum
}

// RandomToken returns a cryptographically strong random token string.
// The Token is generated from 512 random bits and encoded via base32.StdEncoding
func RandomToken() string {
	rnd := make([]byte, 64)

	_, err := rand.Read(rnd)
	if err != nil {
		panic(err)
	}

	return strings.Trim(base32.StdEncoding.EncodeToString(rnd), "=")
}
