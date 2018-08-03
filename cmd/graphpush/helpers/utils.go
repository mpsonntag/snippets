package helpers

import (
	"os"

	"github.com/mpsonntag/snippets/cmd/graphpush/log"
)

// ValidDirectory checks whether a given path exists and refers to a valid directory.
func ValidDirectory(path string) bool {
	var fi os.FileInfo
	var err error
	if fi, err = os.Stat(path); err != nil {
		log.ShowWrite("[Error] checking directory '%s'\n", err.Error())
		return false
	} else if !fi.IsDir() {
		log.ShowWrite("[Error] invalid directory '%s' \n", fi.Name())
		return false
	}
	return true
}
