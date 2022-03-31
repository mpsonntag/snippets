package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func walkgitdirs(annexbinpath, dirpath string) error {
	gitlist := []string{}
	annexInfoList := []AnnexInfo{}
	currwalk := func(currpath string, fio os.FileInfo, err error) error {
		if err != nil {
			fmt.Printf("[E] encountered filepath walk at %s error: %q\n", currpath, err.Error())
			return err
		}
		// ignore files
		if !fio.IsDir() {
			fmt.Printf("[I] Ignoring file %q\n", currpath)
			return filepath.SkipDir
		}

		// check if the current directory is a git directory, bare or otherwise
		// assume the current directory is a bare git repo. stop and do all check stuff required
		if strings.HasSuffix(currpath, ".git") {
			fmt.Printf("[I] current dir %q is a bare repo; skipping\n", currpath)

			aninf, err := infoFromBareRepo(annexbinpath, currpath)
			if err != nil {
				fmt.Printf("[E] handling bare repo info: %q", err.Error())
				return err
			}

			annexInfoList = append(annexInfoList, aninf)
			gitlist = append(gitlist, currpath)
			return filepath.SkipDir
		}
		// check if the current directory is a normal git dir. stop and do all check stuff required
		checkgitpath := filepath.Join(currpath, ".git")
		inf, err := os.Stat(checkgitpath)
		if err != nil && !os.IsNotExist(err) {
			fmt.Printf("[I] err checking git dir, continuer: %q\n", err.Error())
		} else if os.IsNotExist(err) {
			fmt.Println("[I] curr dir has no .git folder, continue")
		} else if inf.IsDir() {
			fmt.Printf("[I] current dir %q is a git dir; skipping\n", currpath)
			gitlist = append(gitlist, currpath)
			return filepath.SkipDir
		}

		fmt.Printf("[I] curr dir %q is no git dir, moving on\n", currpath)
		return nil
	}

	err := filepath.Walk(dirpath, currwalk)
	if err != nil {
		return err
	}

	fmt.Printf("[I] Found the following git dirs: %v\n", gitlist)
	fmt.Printf("[I] Annexinfo: %v\n", annexInfoList)
	return nil
}

func handlebinpath() (string, error) {
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
