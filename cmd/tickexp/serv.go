package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"

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

	data := ExpItem{
		date:  "27.10.2021",
		value: "1.90",
		desc:  "VIE",
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		fmt.Printf("Error rendering template: %s", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

// ResultsPage renders the results
const ResultsPage = `<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="robots" content="noindex,nofollow">
		<meta name="author" content="miso">
		<meta name="description" content="Info">
		<title>tickexp results</title>
	</head>
	<body>
		<h1>Tickexp results page</h1>

		<p>Le grande total: 949-[value]</p>

		<table>
			<thead>
				<tr>
					<th>Date</th>
					<th>Value</th>
					<th>Description</th>
				</tr>
			</thead>
			<tbody>
				{{ range . }}
				<tr>
					<td>{{.Date}}</td>
					<td>{{.Val}}{{.Negval}}</td>
					<td>{{.Desc}}</td>
				</tr>
				{{ end }}
			</tbody>
		</table>
	</body>
</html>`
