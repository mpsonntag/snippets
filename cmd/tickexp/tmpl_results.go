package main

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
					<th>Running Increase</th>
					<th>Description</th>
				</tr>
			</thead>
			<tbody>
				{{ range . }}
				<tr>
					<td>{{.Date}}</td>
					<td>{{.Val}}{{.Negval}}</td>
					<td>{{.Negval}}</td>
					<td>{{.Desc}}</td>
				</tr>
				{{ end }}
			</tbody>
		</table>
	</body>
</html>`
