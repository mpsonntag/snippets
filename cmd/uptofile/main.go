package main

import (
	"bufio"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"
)

const comparelist = "https://raw.githubusercontent.com/mpsonntag/snippets/master/cmd/uptofile/resources/whitelist"

const pagebody = `
{{ define "pagebody" }}
<html>
<body>
{{ template "content" }}
</body>
</html>
{{ end }}
`

const uploadform = `
{{ define "content" }}
<h1>Email address upload form</h1>
<p>Upload comma separated email addresses. Whitespaces and duplicates will be removed.</p>
<form method='post' action='/uploaded'>
	<label for='content'>Email addresses</label>
	<textarea required name='content' id='content'></textarea>
	<label for='password'>Password</label>
	<input required type='password' name='password' id='password' size='50'>
	<input type='submit' value='Submit'>
</form>
{{ end }}
`

const uploaded = `
{{ define "content" }}
<h1>Upload received</h1>
<p><a href='upload'>Back to the upload form</a></p>
{{ end }}
`

var port = ":3030"
var outdir = filepath.Join(os.Getenv("HOME"), "Chaos", "DL")
var password = "iamsecret"

func basicFail() string {
	return `<html>
	<body><h1>500 Internal server error</h1></body>
	</html>`
}

func rootFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "It's alive!")
}

func uploadFormFunc(w http.ResponseWriter, r *http.Request) {
	tmpl := template.New("pagebody")
	tmpl, err := tmpl.Parse(pagebody)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
		return
	}
	tmpl, err = tmpl.Parse(uploadform)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
		return
	}

	w.WriteHeader(http.StatusOK)
	err = tmpl.Execute(w, map[string]interface{}{})
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
	}
}

func processUploadFunc(w http.ResponseWriter, r *http.Request) {
	var outfilepath = filepath.Join(outdir, "outfile.txt")

	content := r.FormValue("content")
	pwd := r.FormValue("password")

	// In case of an invalid password just redirect back to the upload form
	if pwd != password {
		fmt.Fprintln(os.Stdout, "[Warning] Invalid password received")
		http.Redirect(w, r, "/upload", http.StatusSeeOther)
		return
	}

	fmt.Fprintf(os.Stdout, "\n[Info] Received form value: %v\n", content)

	tmpl := template.New("pagebody")
	tmpl, err := tmpl.Parse(pagebody)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
		return
	}
	tmpl, err = tmpl.Parse(uploaded)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
		return
	}

	w.WriteHeader(http.StatusOK)
	err = tmpl.Execute(w, map[string]interface{}{})
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, basicFail())
	}

	// Sanitize input and split on whitespaces, comma and semicolon
	rstring := regexp.MustCompile(`[\s,;]+`)
	sanstring := rstring.ReplaceAllString(content, " ")
	contentslice := strings.Split(sanstring, " ")
	fmt.Fprintf(os.Stdout, "\n[Info] Sanitized, sliced content: '%v'\n\n", contentslice)

	mailmap := make(map[string]interface{})
	// The file is created below if it does not exist yet
	if _, err := os.Stat(outfilepath); err == nil {
		// Read file lines to map for duplicate entry exclusion
		datafile, err := os.Open(outfilepath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\n[Error] Could not open outfile: '%v'\n\n", err)
			return
		}
		fileScanner := bufio.NewScanner(datafile)

		// Populate data map
		for fileScanner.Scan() {
			mailmap[fileScanner.Text()] = nil
		}

		// No defer close since the same file is opened again and truncated below
		datafile.Close()
	}

	// Reconcile stored and new data
	for _, v := range contentslice {
		if val, ok := mailmap[sha1String(v)]; ok {
			fmt.Fprintf(os.Stdout, "\n[Info] Omitting duplicate entry '%v' for address: '%v'\n\n", val, v)
		}
		mailmap[sha1String(v)] = nil
	}
	fmt.Fprintf(os.Stdout, "\n[Info] Sanitized, sliced, hashed content: '%v'\n\n", contentslice)

	// Truncate output file and write all data to it
	outfile, err := os.OpenFile(outfilepath, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n[Error] Could not open outfile for writing: '%v'\n\n", err)
		return
	}
	defer outfile.Close()

	for k := range mailmap {
		if k == "" {
			continue
		}
		fmt.Fprintf(os.Stdout, "\n[Info] Writing '%s' to file\n\n", k)
		_, err = fmt.Fprintln(outfile, k)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\n[Error] Could not write content '%s' to file: '%v'\n\n", k, err)
		}
	}
}

func handleRegistration(w http.ResponseWriter, r *http.Request) {

	compare := sha1String("icanhascheeseburger")

	registered, err := handleWhitelistRegistration(compare)
	if err != nil {
		fmt.Printf("Error handling whitelist: '%s'", err.Error())
		return
	}

	if !registered {
		fmt.Printf("Provided address not in whitelist: '%s'", compare)
		return
	}

	fmt.Printf("Registration address found in whitelist: '%s'\n", compare)
}

func sha1String(content string) string {
	hasher := sha1.New()
	io.WriteString(hasher, content)
	hash := hasher.Sum(nil)
	encoded := hex.EncodeToString(hash[:])

	return encoded
}

func handleWhitelistRegistration(input string) (bool, error) {
	const whitelistlocation = "https://raw.githubusercontent.com/mpsonntag/snippets/master/cmd/uptofile/resources/whitelist"
	compare := sha1String(input)

	resp, err := http.Get(whitelistlocation)
	if err != nil {
		return false, fmt.Errorf("Error fetching whitelist: '%s'", err.Error())
	}

	fmt.Printf("Current response header: '%v'", resp.Header)

	defer resp.Body.Close()

	var registered bool
	respScan := bufio.NewScanner(resp.Body)
	for respScan.Scan() {
		curr := respScan.Text()
		if curr == "" {
			continue
		}
		if curr == compare {
			registered = true
			break
		}
	}
	return registered, nil
}

func main() {
	if _, err := os.Stat(outdir); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "\n[Error] Output directory not found: '%v', abort...\n\n", outdir)
		os.Exit(-1)
	}

	http.HandleFunc("/", rootFunc)
	http.HandleFunc("/upload", uploadFormFunc)
	http.HandleFunc("/uploaded", processUploadFunc)
	http.HandleFunc("/register", handleRegistration)
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
