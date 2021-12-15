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

		<p>
			Base expense: {{ ppfloat .Offsetval }}<br>
			Total additional expenses: {{ ppfloat .Negvalsum }}<br>
			Total benefit expenses: {{ ppfloat .Valsum }}
		</p>
		<hr>
		<p>Goal to reach: {{ legrande .Offsetval .Negvalsum .Valsum }}</p>
		<hr>

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
				{{ range .Data }}
				<tr>
					<td>{{.Date}}</td>
					<td>{{.Val}}</td>
					<td>{{.Negval}}</td>
					<td>{{.Desc}}</td>
				</tr>
				{{ end }}
			</tbody>
		</table>
	</body>
</html>`
