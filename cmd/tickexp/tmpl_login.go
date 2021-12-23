package main

// LoginPage renders the login form
const LoginPage = `<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="robots" content="noindex,nofollow">
		<meta name="author" content="miso">
		<meta name="description" content="Info">
		<title>tickexp login</title>
	</head>
	<body>
		<h1>Tickexp data entry page</h1>
		<form method="POST" action="/login">
			<label for="phrase">Phrase</label>
			<input type="text" name="phrase" id="phrase">
			<label for="pass">Pass</label>
			<input type="password" name="pass" id="pass">
			<input type="hidden" name="reference" id="reference" value="{{ .ReferenceVal }}">
			<input type="submit" value="submit" id="submit">
		</form>
	</body>
</html>`
