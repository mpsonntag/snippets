package main

import (
	"fmt"

	"github.com/spf13/cobra"
)

type gitrepoinfo struct {
	missingAnnex bool
	lockedAnnex bool
	annexSize int
	annexSizeUnit string
	gitSize int
	gitSizeUnit string
}

func checkAnnexComplete(repopath string) (gitrepoinfo, error) {
	// git and git annex commands can only be run from within
	// a git repository. To avoid switching back and forth
	// for multiple git commands, this function collects 
	// all required information and returns a fitting struct.
	log.Printf("Start annex check for repo %q", repopath)
	defer changedirlog("/", "checkAnnexComplete")

	info := gitrepoinfo{}

	// return with error if repo path is not accessible
	err := os.Chdir(repopath)
	if err != nil {
		return info, fmt.Errorf("could not switch to repopath: %s", err.Error())
	}

	// missing content check
	stdout, stderr, err := annexCMD(repopath, "find", "--not", "--in=here")
	if err != nil {
		log.Printf("error checking missing annex content: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found missing annex files: %s, %s, %s", err.Error(), stdout, stderr)
		info.missingAnnex = true
	}

	// locked content check
	stdout, stderr, err = annexCMD(repopath, "find", "--locked")
	if err != nil {
		log.Printf("error checking locked annex content: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found locked annex files: %s, %s, %s", err.Error(), stdout, stderr)
		info.lockedAnnex = true
	}

	// annex size check
	stdout, stderr, err = annexCMD(repopath, "info", "--fast", ".")
	if err != nil {
		log.Printf("error checking annex content size: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found annex file size: %s, %s, %s", err.Error(), stdout, stderr)
	}

	// git size check
	stdout, stderr, err = gitCMD(repopath, "count-objects", "-H")
	if err != nil {
		log.Printf("error checking annex content size: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found git file size: %s, %s, %s", err.Error(), stdout, stderr)
	}

	return info, nil
}

func runannexcheck() {
	// check repository annex content
	incompleteContent, err := checkAnnexComplete(repodir)

	// skip zip creation when an annex content issue has been found
	if err != nil {
		return "", -1, fmt.Errorf("skipping zip creation, error checking annex content: %s", err.Error())
	}

	if incompleteContent.missingAnnex {
		return "", -1, fmt.Errorf("skipping zip creation, found missing annex file content: %s", err.Error())
	}

	if incompleteContent.missingAnnex {
		return "", -1, fmt.Errorf("skipping zip creation, found missing annex file content: %s", err.Error())
	}

	// on repo access error or missing content error stop and return appropriate err message

	// on locked content but no missing annex data check repo size

	// if repo size > cutoff size (500 GB) stop and return with an error
	//if reposize > cutoff {
	//	return 
	//}

	// if repo size <= cutoff size (500 GB) create directory copy, unlock all files and create zip file from there
	//if reposize <= cutoff {
	//	cpdir := fmt.Sprintf("%s_unlocked", repodir)
	//	import "os/exec"
	//	log.Printf("copy locked content directory to %q", cpdir)
	//	cmd := exec.Command("cp", "--recursive", repodir, cpdir)
	//	err = cmd.Run()
	//	if err != nil {
	//		return "", -1, fmt.Errorf("skipping zip creation, error copying locked content dir: %s", err.Error())
	//	}
	//	repodir = cpdir
	//	// switch to cp dir and unlock annex files
	//	
	//}
}

func setUpCommands(verstr string) *cobra.Command {
	var rootCmd = &cobra.Command{
		Use:                   "annexcheck",
		Long:                  "annexcheck",
		Version:               fmt.Sprintln("0.0.1"),
		DisableFlagsInUseLine: true,
	}
	cmds := make([]*cobra.Command, 1)
	cmds[0] = &cobra.Command{
		Use:                   "run",
		Short:                 "run the annexcheck from the current directory",
		Args:                  cobra.NoArgs,
		Run:                   runannexcheck,
		Version:               fmt.Sprintln("0.0.1"),,
		DisableFlagsInUseLine: true,
	}

	rootCmd.AddCommand(cmds...)

	return rootCmd
}

func main() {
	fmt.Println("...[I] parsing CLI")

	err := rootCmd.Execute()
	if err != nil {
		fmt.Printf("...[E] running tickexp: %q\n", err.Error())
	}
}
