package helpers

import (
	"bytes"
	"os"
	"os/exec"
	"strconv"

	"github.com/mpsonntag/snippets/cmd/graphpush/log"
)

// IsValidPort checks whether a provided port value can be parsed into a valid
// server port number (uint16)
func IsValidPort(port string) bool {
	_, err := strconv.ParseUint(port, 10, 16)
	return err == nil
}

// AppVersionCheck tries to execute a shell command with commandline argument
// "--version" and returns the resulting commandline output or the error if
// one occurs.
func AppVersionCheck(binpath string) (string, error) {
	cmd := exec.Command(binpath, "--version")
	var out bytes.Buffer
	cmd.Stdout = &out
	if err := cmd.Run(); err != nil {
		return "", err
	}
	return out.String(), nil
}

// ValidDirectory checks whether a given path exists and refers to a valid directory.
func ValidDirectory(path string) bool {
	var fi os.FileInfo
	var err error
	if fi, err = os.Stat(path); err != nil {
		log.ShowWrite("[Error] checking directory '%s': '%s'\n", path, err.Error())
		return false
	} else if !fi.IsDir() {
		log.ShowWrite("[Error] invalid directory '%s'\n", fi.Name())
		return false
	}
	return true
}
