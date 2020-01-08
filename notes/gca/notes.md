# Notes on dev and testing

## Database

### Database updates
When updating the postgres database make sure that the service is restarted after the 
update it done, otherwise the play service might have a stale view on the database service.
