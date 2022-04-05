package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
)

type AnnexInfo struct {
	RepoName string
	Branches string
	Missing  []string
	Size     string
}

type RepoInfoCMD struct {
	// provides the information whether annex has been identified
	AnnexAvailable bool
	// provides the information whether the host natively provides annex
	HostAnnexAvailable bool
	// provides the (absolute) path where the binary can find the
	// annex binaries locally if it is not provided by the host
	LocalAnnexPath string
}

func (repin *RepoInfoCMD) init(annexpath string) error {
	if annexpath != "" {
		// --- could add more safeguards at this point
		ok, err := annexAvailable(annexpath)
		if ok && err == nil {
			// the host provides annex, how nice
			repin.AnnexAvailable = true
			repin.LocalAnnexPath = annexpath
			return nil
		}
		if err != nil {
			// no worries, just print the error and continue
			fmt.Printf("[E] handling custom annex path %s\n", err.Error())
		}
	}

	// check whether the host provides annex natively
	ok, err := annexAvailable("")
	if ok && err == nil {
		// the host provides annex, how nice
		repin.AnnexAvailable = true
		repin.HostAnnexAvailable = true
		return nil
	}
	if err != nil {
		// no worries, just print the error and continue
		fmt.Printf("just an info %s\n", err.Error())
	}
	fmt.Println("[I] the host does not provide annex")

	// check whether the annex binary can be found next to the executable
	annexpath, err = identifyAnnexBinPath()
	if err != nil {
		return err
	}

	fmt.Printf("[I] using available annex at %q\n", annexpath)
	repin.AnnexAvailable = true
	repin.LocalAnnexPath = annexpath
	return nil
}

func (repin *RepoInfoCMD) walkgitdirs(dirpath string) error {
	if !repin.AnnexAvailable {
		return fmt.Errorf("[E] could not verify annex walking dir %q", dirpath)
	}

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

			aninf, err := infoFromBareRepo(repin.LocalAnnexPath, currpath)
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

func handleAnnexFlag(cmd *cobra.Command, flagname string) (string, error) {
	annexpath, err := cmd.Flags().GetString("annexdir")
	if err != nil {
		return "", fmt.Errorf("[E] parsing custom annex flag: %s", err.Error())
	}
	absannexpath, err := filepath.Abs(annexpath)
	if err != nil {
		return "", fmt.Errorf("[E] determining absolute path for %s: %s", absannexpath, err.Error())
	}
	if _, err := os.Stat(absannexpath); os.IsNotExist(err) {
		return "", fmt.Errorf("[E] could not find directory %q, %s", absannexpath, err.Error())
	}
	return absannexpath, nil
}

func handleRootDirFlag(cmd *cobra.Command) (string, error) {
	dirpath, err := cmd.Flags().GetString("checkdir")
	if err != nil {
		return "", fmt.Errorf("[E] parsing directory flag: %s", err.Error())
	}
	gitdirs, err := filepath.Abs(dirpath)
	if err != nil {
		return "", fmt.Errorf("[E] could not get absolute path for %q: %s", dirpath, err.Error())
	}
	if _, err := os.Stat(gitdirs); os.IsNotExist(err) {
		return "", fmt.Errorf("[E] could not find directory %q, %s", gitdirs, err.Error())
	}
	return gitdirs, nil
}

func repoinfocmd(cmd *cobra.Command, args []string) {
	// handle cli root directory flag
	annexpath, err := handleAnnexFlag(cmd, "annexdir")
	if err != nil {
		fmt.Printf("%s\n", err.Error())
		annexpath = ""
	}

	// might be worth check if the next two lines could be replace by a "New" method
	collector := RepoInfoCMD{}
	// annex availability check and repoinfo init comes first
	// exit when annex cannot be found
	err = collector.init(annexpath)
	if err != nil {
		fmt.Printf("%s\n", err.Error())
		os.Exit(1)
	}

	// handle cli root directory flag
	dirpath, err := cmd.Flags().GetString("checkdir")
	if err != nil {
		fmt.Printf("[E] parsing directory flag: %s\n", err.Error())
	}
	gitdirs, err := filepath.Abs(dirpath)
	if err != nil {
		fmt.Printf("[E] could not get absolute path for %s: %s\n", dirpath, err.Error())
		os.Exit(1)
	}
	if _, err := os.Stat(gitdirs); os.IsNotExist(err) {
		fmt.Printf("[E] could not find directory %q, %s\n", gitdirs, err.Error())
		os.Exit(1)
	}
	fmt.Printf("[I] using directory %q\n", gitdirs)

	// walk the directory tree to collect git repository information
	err = collector.walkgitdirs(gitdirs)
	if err != nil {
		fmt.Printf("[E] walking directories: %s\n", err.Error())
	}
}
