# libgin project structure and function usage

libgin is a core library used by various other gin related libraries.
- gin-dex
- gin-doi
- gin-cli
- G-Node/gogs

## Structure

- doi.go

## doi.go

- func RepoPathToUUID   ... used in gogs; has a duplicate function in gin-doi: ´util.go:makeUUID´
- type DOIRegInfo       ... marked as obsolete, but still happily used in gogs to display datacite file content

## archive/archive

- func MakeZip          ... used in gin-doi

