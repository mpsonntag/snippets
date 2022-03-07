package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"

	gingit "github.com/G-Node/gin-cli/git"
	"github.com/spf13/cobra"
)

// annexCMD runs the passed git annex command arguments.
// The command returns stdout and stderr as strings and any error that might occur.
func annexCMD(annexargs ...string) (string, string, error) {
	log.Printf("Running annex command: %s\n", annexargs)
	cmd := gingit.AnnexCommand(annexargs...)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

// annexAvailable checks whether annex is available to the gin client library.
// The function returns false with no error, if the annex command execution
// ends with the git message that 'annex' is not a git command.
// It will return false and the error message on any different error.
func annexAvailable() (bool, error) {
	_, stderr, err := annexCMD("version")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

// remoteGitCMD runs a git command for a given directory
// If the useannex flag is set to true, the executed command
// will be a git annex command instead of a regular git command.
func remoteGitCMD(gitdir string, useannex bool, gitcmd ...string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}

	cmdstr := append([]string{"git", "-C", gitdir}, gitcmd...)
	cmd := gingit.Command("version")
	cmd.Args = cmdstr
	if useannex {
		cmdstr = append([]string{"git", "-C", gitdir, "annex"}, gitcmd...)
		cmd = gingit.AnnexCommand("version")
		cmd.Args = cmdstr
	}
	fmt.Printf("using command: %v, %v\n", gitcmd, cmdstr)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

func missingAnnexContent(gitdir string) (bool, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return false, "", fmt.Errorf("path not found %q", gitdir)
	}
	// command should not return with an error or with any stderr content
	// If stdout is empty, there is no missing content. If it is not empty,
	// the number of lines correspond to the number of files with missing content.
	stdout, stderr, err := remoteGitCMD(gitdir, true, "find", "--not", "--in=here")
	if err != nil {
		return false, "", err
	} else if string(stderr) != "" {
		return false, "", fmt.Errorf("git annex error: %s", string(stderr))
	} else if string(stdout) == "" {
		return false, "", nil
	}
	return true, string(stdout), nil
}

func lockedAnnexContent(gitdir string) (bool, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return false, "", fmt.Errorf("path not found %q", gitdir)
	}
	// command should not return with an error or with any stderr content
	// If stdout is empty, there is no locked content. If it is not empty,
	// the number of lines correspond to the number of files with locked content.
	stdout, stderr, err := remoteGitCMD(gitdir, true, "find", "--locked")
	if err != nil {
		return false, "", err
	} else if string(stderr) != "" {
		return false, "", fmt.Errorf("git annex error: %s", string(stderr))
	} else if string(stdout) == "" {
		return false, "", nil
	}
	return true, string(stdout), nil
}

func annexSize(gitdir string) (string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", fmt.Errorf("path not found %q", gitdir)
	}
	// command should not return with an error or with any stderr content
	stdout, stderr, err := remoteGitCMD(gitdir, true, "info", "--fast", ".")
	if err != nil {
		return "", err
	} else if string(stderr) != "" {
		return "", fmt.Errorf("git annex error: %s", string(stderr))
	} else if string(stdout) == "" {
		return "", nil
	}

	// annex should return the total size of files in the working tree
	splitsizes := strings.Split(stdout, "size of annexed files in working tree: ")
	if len(splitsizes) != 2 {
		return "", nil
	}
	return strings.TrimSpace(splitsizes[1]), nil
}

func acceptedAnnexSize(annexSize string) bool {
	sizesplit := strings.Split(annexSize, " ")
	if len(sizesplit) != 2 {
		return false
	}
	// add check if sizesplit[0] is contained in accepted order
	// checkaccepted := []string{"bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"}
	// if !acceptedorder[sizesplit[1]] { return false }
	// checksize := float32(sizesplit[0])
	checksize := 100.1

	if sizesplit[1] == "terabytes" {
		return false
	} else if sizesplit[1] == "gigabytes" && checksize > 100 {
		return false
	}

	return true
}

func annexContentCheck(repopath string) error {
	// check if there is missing or locked annex content
	log.Printf("Checking missing annex content of repo at %q", repopath)
	hasmissing, misslist, err := missingAnnexContent(repopath)
	if err != nil {
		log.Printf("Could assertain missing annex content: %q", err.Error())
	}
	haslocked, locklist, err := lockedAnnexContent(repopath)
	if err != nil {
		log.Printf("Could assertain locked annex content: %q", err.Error())
	}
	var annexIssues string
	if hasmissing {
		splitmis := strings.Split(strings.TrimSpace(misslist), "\n")
		annexIssues = fmt.Sprintf("found missing content in %d files\n", len(splitmis))
	}
	if haslocked {
		splitlock := strings.Split(strings.TrimSpace(locklist), "\n")
		annexIssues += fmt.Sprintf("found locked content in %d files\n", len(splitlock))
	}
	// we found annex issues, log, do not create zip file and return
	if annexIssues != "" {
		log.Printf("Skip zip, annex content issues have been identified (missing %t, locked %t)", hasmissing, haslocked)
		return fmt.Errorf("annex content issues have been identified, skipping zip creation\n%s", annexIssues)
	}
	return nil
}

func duplicateAnnex(reponame, gitcloneroot, gitrepodir string) error {
	clonename := fmt.Sprintf("%s_unlocked", reponame)
	clonedir := filepath.Join(gitcloneroot, clonename)
	log.Printf("Locally cloning repo %s to dir %s", gitrepodir, clonedir)

	// Clone annex repository to specified clone directory
	// Git clone outputs everything to stderr
	stdout, stderr, err := remoteGitCMD(gitcloneroot, false, "clone", gitrepodir, clonename)
	if err != nil {
		log.Printf("Error cloning annex repo %s: %q, %q", gitrepodir, err.Error(), stderr)
		return fmt.Errorf("error cloning annex repo %s: %q, %q", gitrepodir, err.Error(), stderr)
	}
	log.Printf("Repo %s locally cloned: %q, %q", gitrepodir, stdout, stderr)

	// Copy annex content to clone directory
	stdout, stderr, err = remoteGitCMD(clonedir, true, "copy", "--all", "--from=origin")
	if err != nil {
		log.Printf("Error on local annex (%s) content copy: %q, %q", clonedir, err.Error(), stderr)
		return fmt.Errorf("error on local annex (%s) content copy: %q, %q", clonedir, err.Error(), stderr)
	} else if stderr != "" {
		log.Printf("Error output on local annex (%s) content copy: %q", clonedir, stderr)
		return fmt.Errorf("error output on local annex (%s) content copy: %q", clonedir, stderr)
	}
	log.Printf("Annex content locally copied: %s", stdout)

	// re-check missing annex content in clone directory; should be false
	hasmissing, missinglist, err := missingAnnexContent(clonedir)
	if err != nil {
		log.Printf("Error checking missing annex content on local copy: %q", err.Error())
		return fmt.Errorf("error checking missing annex content on local copy: %q", err.Error())
	} else if hasmissing {
		log.Printf("Missing annex content after local copy: %s", missinglist)
		return fmt.Errorf("missing annex content after local copy: %s", missinglist)
	}
	log.Println("No missing annex content on local copy")

	// unlock all locked annex files in clone directory
	stdout, stderr, err = remoteGitCMD(clonedir, true, "unlock")
	if err != nil {
		log.Printf("Error unlocking files on local copy: %q, %q", err.Error(), stderr)
		return fmt.Errorf("error unlocking files on local copy: %q, %q", err.Error(), stderr)
	} else if stderr != "" {
		log.Printf("Error output unlocking files on local copy: %q", stderr)
		return fmt.Errorf("error output unlocking files on local copy: %q", stderr)
	}
	log.Printf("Unlocked annex file content in clone directory: %s", stdout)

	// re-check locked content
	haslocked, lockedlist, err := lockedAnnexContent(clonedir)
	if err != nil {
		log.Printf("Error checking locked content on local copy: %q", err.Error())
		return fmt.Errorf("error checking locked content on local copy: %q", err.Error())
	} else if haslocked || lockedlist != "" {
		log.Printf("Found locked content after unlocking: %q", lockedlist)
		return fmt.Errorf("found locked content after unlocking: %q", lockedlist)
	}

	return nil
}

// gitCMD runs the passed git command arguments.
// The command returns stdout and stderr as strings and any error that might occur.
func gitCMD(gitargs ...string) (string, string, error) {
	log.Printf("Running git command: %s\n", gitargs)
	cmd := gingit.Command(gitargs...)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

type gitrepoinfo struct {
	missingAnnex bool
	lockedAnnex  bool
}

func checkAnnexComplete(repopath string) (gitrepoinfo, error) {
	log.Printf("Start annex check for repo %q", repopath)

	info := gitrepoinfo{}

	// missing content check
	stdout, stderr, err := remoteGitCMD(repopath, true, "find", "--not", "--in=here")
	if err != nil {
		log.Printf("error checking missing annex content: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found missing annex files: %s, %s, %s", err.Error(), stdout, stderr)
		info.missingAnnex = true
	}

	// locked content check
	stdout, stderr, err = remoteGitCMD(repopath, true, "find", "--locked")
	if err != nil {
		log.Printf("error checking locked annex content: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found locked annex files: %s, %s, %s", err.Error(), stdout, stderr)
		info.lockedAnnex = true
	}

	// annex size check
	stdout, stderr, err = remoteGitCMD(repopath, true, "info", "--fast", ".")
	if err != nil {
		log.Printf("error checking annex content size: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found annex file size: %s, %s, %s", err.Error(), stdout, stderr)
	}

	// git size check
	stdout, stderr, err = remoteGitCMD(repopath, false, "count-objects", "-H")
	if err != nil {
		log.Printf("error checking git content size: %s, %s, %s", err.Error(), stdout, stderr)
	}
	if len(stdout) > 0 {
		log.Printf("found git file size: %s, %s, %s", err.Error(), stdout, stderr)
	}

	// remove once fully refactored and the issues return on error
	if err != nil {
		return info, err
	}

	return info, nil
}

func runannexcheck(repodir string) (string, error) {
	if _, err := os.Stat(repodir); os.IsNotExist(err) {
		return "", fmt.Errorf("path not found %q", repodir)
	}

	// check repository annex content
	incompleteContent, err := checkAnnexComplete(repodir)

	// skip zip creation when an annex content issue has been found
	if err != nil {
		return "", fmt.Errorf("skipping zip creation, error checking annex content: %s", err.Error())
	}

	if incompleteContent.missingAnnex {
		return "", fmt.Errorf("skipping zip creation, found missing annex file content: %s", err.Error())
	}

	if incompleteContent.missingAnnex {
		return "", fmt.Errorf("skipping zip creation, found missing annex file content: %s", err.Error())
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

	return "all good", nil
}

func clicall(cmd *cobra.Command, args []string) {
	repodir := "/home/sommer/Chaos/DL/annextmp"
	_, err := runannexcheck(repodir)
	if err != nil {
		log.Printf("error running annexcheck: %q", err.Error())
	}
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
		Run:                   clicall,
		Version:               fmt.Sprintln("0.0.1"),
		DisableFlagsInUseLine: true,
	}

	rootCmd.AddCommand(cmds...)

	return rootCmd
}

func main() {
	fmt.Println("...[I] parsing CLI")

	cmds := setUpCommands("")
	err := cmds.Execute()
	if err != nil {
		fmt.Printf("...[E] running annexcheck: %q\n", err.Error())
	}
}
