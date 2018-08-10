from urllib import request

searchterm = "electrode"
usrkey = "ZRt6argPOzoqCwk8ULK5N7agk731VsZy"

resp = request.urlopen("https://scicrunch.org/api/1/ilx/search/term/%s?key=%s" %
                       (searchterm, usrkey))

print("Status response: '%s'; length: %s" % (resp.msg, resp.length()))

content = resp.read()

print("Content:\n%s\n" % content)
