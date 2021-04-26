### GIN-DOI deployment checklist

This document describes the manual tests that should be run in the
dev and test deployment before deploying a new version of the 
gin-doi server to the live machine.

Make sure to push and deploy the latest build to the dev and test 
environment and keep an eye on the gin-doi logfile before starting to
run the tests:

```bash
# Run the command from the folder containing the gin-doi docker-compose file
docker-compose logs -f --tail=200
```
