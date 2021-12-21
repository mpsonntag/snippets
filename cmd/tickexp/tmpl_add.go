package main

// AddPage renders the data entry form
const AddPage = `<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="robots" content="noindex,nofollow">
		<meta name="author" content="miso">
		<meta name="description" content="Info">
		<title>tickexp data entry</title>
		<style>
			input:invalid {
				border: red solid 3px;
			}
		</style>
	</head>
	<body>
		<h1>Tickexp data entry page</h1>
		<form method="POST" action="/dataadd">
			<label for="date">Date</label>
			<input type="text" name="date" id="date"
					value="{{ currdate }}"
					pattern="{{ regexpdate }}" 
					required minlength="10" maxlength="10" size="10">
			<label for="val">Value</label>
			<input type="text" name="val" id="val" 
					placeholder="supported: 11.11-11.11" 
					pattern="{{ regexpval }}">
			<label for="desc">Description</label>
			<input type="text" name="desc" id="desc">
			<input type="submit" value="submit" id="submit">
		</form>

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
				{{ range . }}
				<tr>
					<td>{{ .Date }}</td>
					<td>{{ .Val }}</td>
					<td>{{ .Negval }}</td>
					<td>{{ .Desc }}</td>
				</tr>
				{{ end }}
			</tbody>
		</table>
	</body>
</html>`
