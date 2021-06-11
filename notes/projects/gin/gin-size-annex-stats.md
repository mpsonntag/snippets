
## Potential workflow

- reposizes `update` python script creates json file
- annexcheck creates annex content output for a specific repo

- wrapper script
  - checks which directories have been changed within a given timeframe
  - runs reposize functions on these repos and writes output to json file -> only changes content for these directories
  - runs annexcheck for these directories and updates a new json that contains info on annex content yes/no, annex content missing yes/no + file list -> specify format below
  
  - always write to file copy first and replace once writing has finished to minimize
  - merge json for both outputs

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
