## Notes for the "meta" server source file updates

This repository contains the scripts required to update the "meta" server with new data from CRCNS or G-Node published via datacite.

Make sure the script runs in an environment that has Python >3.8 and that its not a problem when additional packages are installed.

The `meta_source_from_datacite` script can be run from the command line. Ideally redirect the output to a log file and monitor it for errors.

    bash meta_source_from_datacite > meta_from_datacite.log
    tail -f meta_from_datacite.log

Since the script requires multiple steps and online queries it can take a while.

The script should be set up to never overwrite existing files in the `odml` or `rdf` folders. Do not commit any changes that edit existing files in these folders but check the logfile and investigate. Commit only new files.

Provided no RDF files are overwritten, keeping the odml IDs intact and unchanged, all files in the `rdf` folder can be uploaded to the RDF server. Duplicate entries will not be added to the database.

The files have to be manually uploaded at the hidden administrative panel meta.g-node.org/manage.html using the "upload data" feature. The upload requires the admin password that can be found either in the shiroi.ini file on the server or the gnode password database.
