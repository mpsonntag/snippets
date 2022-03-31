package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func identifyAnnexBinPath() (string, error) {
	binpath, err := os.Executable()
	if err != nil {
		return "", fmt.Errorf("[E] fetching executable path: %s", err.Error())
	}
	if _, err := os.Stat(binpath); os.IsNotExist(err) {
		return "", fmt.Errorf("[E] executable path could not be identified: %s", err.Error())
	}

	binname := filepath.Base(binpath)
	annexpath := strings.Replace(binpath, binname, "git-annex.linux", 1)

	if _, err := os.Stat(annexpath); err != nil {
		return "", fmt.Errorf("[E] annex binary path %q not found: %s", annexpath, err.Error())
	}

	// check if annex is available; exit otherwise
	ok, err := annexAvailable(annexpath)
	if err != nil {
		return "", fmt.Errorf("[E] checking annex at %q: %s", annexpath, err.Error())
	}

	if !ok {
		return "", fmt.Errorf("[E] annex is not available at %q", annexpath)
	}
	return annexpath, nil
}
