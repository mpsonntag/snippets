package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"
)

var tmplfuncs = template.FuncMap{
	"Upper":   strings.ToUpper,
	"Replace": strings.ReplaceAll,
}

var templateMap = map[string]string{
	"Nav":    "",
	"Footer": "",
}

// ALNUM provides characters for the randAlnum function.
// Excluding 0aou to avoid the worst of swear words turning up by chance.
const ALNUM = "123456789bcdefghijklmnpqrstvwxyz"

// randAlnum returns a random alphanumeric (lowercase, latin) string of length 'n'.
// Negative numbers return an empty string.
func randAlnum(n int) string {
	if n < 0 {
		return ""
	}

	N := len(ALNUM)

	chrs := make([]byte, n)
	rand.Seed(time.Now().UnixNano())
	for idx := range chrs {
		chrs[idx] = ALNUM[rand.Intn(N)]
	}

	candidate := string(chrs)
	// return string has to contain at least one number and one character
	// if the required string length is larger than 1.
	if n > 1 {
		renum := regexp.MustCompile("[1-9]+")
		rechar := regexp.MustCompile("[bcdefghijklmnpqrstvwxyz]+")
		if !renum.MatchString(candidate) || !rechar.MatchString(candidate) {
			log.Printf("Re-running radnAlnum: %s", candidate)
			candidate = randAlnum(n)
		}
	}

	return candidate
}

// readFileAtPath returns the content of a file at a given path.
func readFileAtPath(path string) ([]byte, error) {
	fp, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	defer fp.Close()

	stat, err := fp.Stat()
	if err != nil {
		return nil, err
	}
	contents := make([]byte, stat.Size())
	_, err = fp.Read(contents)
	return contents, err
}

// readFileAtURL returns the contents of a file at a given URL.
func readFileAtURL(url string) ([]byte, error) {
	client := &http.Client{}
	log.Printf("Fetching file at %q", url)
	req, _ := http.NewRequest(http.MethodGet, url, nil)
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Request failed: %s", err.Error())
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("request returned non-OK status: %s", resp.Status)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Printf("Could not read file contents: %s", err.Error())
		return nil, err
	}
	return body, nil
}

// prepareTemplates initialises and parses a sequence of templates in the order
// they appear in the arguments.  It always adds the Nav template first and
// includes the common template functions in tmplfuncs.
func prepareTemplates(templateNames ...string) (*template.Template, error) {
	tmpl, err := template.New("Nav").Funcs(tmplfuncs).Parse(templateMap["Nav"])
	if err != nil {
		log.Printf("Could not parse the \"Nav\" template: %s", err.Error())
		return nil, err
	}
	tmpl, err = tmpl.New("Footer").Parse(templateMap["Footer"])
	if err != nil {
		log.Printf("Could not parse the \"Footer\" template: %s", err.Error())
		return nil, err
	}
	for _, tName := range templateNames {
		tContent, ok := templateMap[tName]
		if !ok {
			return nil, fmt.Errorf("unknown template with name %q", tName)
		}
		tmpl, err = tmpl.New(tName).Parse(tContent)
		if err != nil {
			log.Printf("Could not parse the %q template: %s", tName, err.Error())
			return nil, err
		}
	}
	return tmpl, nil
}
