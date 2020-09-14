package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"text/template"
)

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
	<input required type='email' multiple name='content' id='content' size='50'>
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

	// Sanitize input and split on comma
	contentslice := strings.Split(strings.ReplaceAll(content, " ", ""), ",")
	fmt.Fprintf(os.Stdout, "\n[Info] Sanitized, sliced content: '%v'\n\n", contentslice)

	var filedata string

	// Read file data for exclusion of duplicates
	if _, err := os.Stat(outfilepath); err == nil {
		data, err := ioutil.ReadFile(outfilepath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "\n[Error] Could not open outfile: '%v'\n\n", err)
			return
		}
		filedata = string(data)

		fmt.Fprintf(os.Stdout, "\n[Info] File content: '%s'", filedata)
	}

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
		if strings.Contains(filedata, v) {
			fmt.Fprintf(os.Stdout, "\n[Info] Excluding existing value '%s'\n\n", v)
			continue
		}
		fmt.Fprintf(os.Stdout, "\n[Info] Writing value '%s' to file\n\n", v)
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
