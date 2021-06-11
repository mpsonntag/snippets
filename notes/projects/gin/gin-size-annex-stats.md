
## Potential workflow

- reposizes `update` python script creates json file
- annexcheck creates annex content output for a specific repo

- wrapper script
  - checks which directories have been changed within a given timeframe
  - runs reposize functions on these repos and writes output to json file -> only changes content for these directories
  - runs annexcheck for these directories and updates a new json that contains info on annex content yes/no, annex content missing yes/no + file list -> specify format below
  - add list of users that do not have any repositories
  - add "json" output option to the annexcheck script

  - always write to file copy first and replace once writing has finished to minimize
  - merge json for both outputs

One may find changed directories with the following snippet; this finds
- changed directories only
- to a max directory depth of 2 (repo owner and repo name) - since the server contains only bare repos (only git content); if any change occurred, the whole folder should be updated
- directories that contain changes within the last 10 minitues
- if an absolute path is given, the output will be absolute paths as well.
- could be piped to annexcheck or any other script?
```bash
find /absolute/path/to/gin/repos/gin-repositories -maxdepth 2 -mmin -10 -type d
```

## annex json format

{
  "[repo owner]/[repo name]": {
    "annex_content": true/false,
    "annex_content_missing": true/false,
    "missing_list": [
      "file_A",
      "file_B",
      "file_C"
    ]
  }
}
