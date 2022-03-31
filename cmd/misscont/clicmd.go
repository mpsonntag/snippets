package main

import (
	"fmt"
	"os"
	"path/filepath"

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
func repoinfocmd(cmd *cobra.Command, args []string) {
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

	err = walkgitdirs("", gitdirs)
	if err != nil {
		fmt.Printf("[E] walking directories: %s\n", err.Error())
	}
}
