package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	gingit "github.com/G-Node/gin-cli/git"
	"github.com/spf13/cobra"
)

func utilInitAnnex(gitdir string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}

	cmd := gingit.AnnexCommand()
	cmd.Args = []string{"git", "-C", gitdir, "annex", "init"}
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
func remoteGitCMD(gitdir string, useannex bool, gitcmd... string) (string, string, error) {
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

// gitCMD changes the working directory to a provided git directory
// and runs a git command by prepending 'git ' to passed
// git commands.
// It returns stdout, stderr as strings and any error that might occur.
func gitCMD(gitdir string, gitcommand ...string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}
	if err := os.Chdir(gitdir); err != nil {
		return "", "", fmt.Errorf("failed to access git dir %q: %q", gitdir, err.Error())
	}

	log.Printf("Running git command: %s", gitcommand)
	cmd := gingit.Command(gitcommand...)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

// annexCMD changes the working directory to a provided git directory
// and runs an annex command by prepending 'git annex' to passed
// annex commands.
// It returns stdout, stderr as strings and any error that might occur.
func annexCMD(gitdir string, annexcommand ...string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}
	if err := os.Chdir(gitdir); err != nil {
		return "", "", fmt.Errorf("failed to access annex dir %q: %q", gitdir, err.Error())
	}

	log.Printf("Running annex command: %s", annexcommand)
	cmd := gingit.AnnexCommand(annexcommand...)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

type gitrepoinfo struct {
	missingAnnex  bool
	lockedAnnex   bool
	annexSize     int
	annexSizeUnit string
	gitSize       int
	gitSizeUnit   string
}

func missingAnnexContent(gitdir string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}

	//log.Printf("Running missing annex command: %q", []string{"-C", gitdir, "annex", "find", "--not", "--in=here"})
	//cmd := gingit.AnnexCommand("-C", gitdir, "annex", "find", "--not", "--in=here")
	//fmt.Printf("blaaaaaargh %s", cmd.Args)
	cmd := gingit.AnnexCommand("info")
	cmd.Args = []string{"git", "-C", gitdir, "annex", "find", "--not", "--in=here"}
	fmt.Printf("These are the command args: %s", cmd.Args)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

func someRemoteAnnex(gitdir string, gitcmd ...string) (string, string, error) {
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return "", "", fmt.Errorf("path not found %q", gitdir)
	}

	//log.Printf("Running missing annex command: %q", []string{"-C", gitdir, "annex", "find", "--not", "--in=here"})
	//cmd := gingit.AnnexCommand("-C", gitdir, "annex", "find", "--not", "--in=here")
	//fmt.Printf("blaaaaaargh %s", cmd.Args)
	cmd := gingit.AnnexCommand("info")
	cmd.Args = append([]string{"git", "-C", gitdir, "annex"}, gitcmd...)
	fmt.Printf("These are the command args: %s", cmd.Args)
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

func checkAnnexComplete(repopath string) (gitrepoinfo, error) {
	// git and git annex commands can only be run from within
	// a git repository. To avoid switching back and forth
	// for multiple git commands, this function collects
	// all required information and returns a fitting struct.
	log.Printf("Start annex check for repo %q", repopath)

	info := gitrepoinfo{}

	// missing content check
	stdout, stderr, err := missingAnnexContent(repopath)
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

func checkAnnexCompleteOld(repopath string) (gitrepoinfo, error) {
	// git and git annex commands can only be run from within
	// a git repository. To avoid switching back and forth
	// for multiple git commands, this function collects
	// all required information and returns a fitting struct.
	log.Printf("Start annex check for repo %q", repopath)

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

// changedirlog logs if a change directory action results in an error;
// used to log errors when defering directory changes.
func changedirlog(todir string, lognote string) {
	err := os.Chdir(todir)
	if err != nil {
		log.Printf("%s: %s; could not change to dir %s", err.Error(), lognote, todir)
	}
}

func runannexcheckOld(repodir string) (string, error) {
	if _, err := os.Stat(repodir); os.IsNotExist(err) {
		return "", fmt.Errorf("path not found %q", repodir)
	}

	// not sure this dir switch back is required; at best it should
	// be done when the whole process has finished.
	defer changedirlog("/", "checkAnnexComplete")

	// check repository annex content
	incompleteContent, err := checkAnnexCompleteOld(repodir)

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
	_, err := runannexcheckOld(repodir)
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
