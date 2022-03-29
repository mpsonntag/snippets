package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/G-Node/gin-cli/git/shell"
)

// AnnexCommand sets up a git annex command with the provided arguments and returns a GinCmd struct.
func remoteAnnexCommand(annexbinpath string, gitdir string, args ...string) (shell.Cmd, error) {
	if _, err := os.Stat(annexbinpath); os.IsNotExist(err) {
		return shell.Cmd{}, fmt.Errorf("annex path not found %q", annexbinpath)
	}
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return shell.Cmd{}, fmt.Errorf("gitdir path not found %q", gitdir)
	}
	gitannexpath := annexbinpath

	cmdstr := append([]string{"-C", gitdir, "annex"}, args...)
	cmd := shell.Command("git", cmdstr...)

	// make sure the local annex is available to the command
	env := os.Environ()
	syspath := os.Getenv("PATH")
	syspath += string(os.PathListSeparator) + gitannexpath
	cmd.Env = append(env, syspath)

	workingdir, _ := filepath.Abs(".")
	fmt.Printf("Running shell command (Dir: %s): %s", workingdir, strings.Join(cmd.Args, " "))

	return cmd, nil
}

// annexCMD runs the passed git annex command arguments.
// The command returns stdout and stderr as strings and any error that might occur.
func annexCMD(annexbinpath string, gitdir string, annexargs ...string) (string, string, error) {
	fmt.Printf("Running annex command: %s\n", annexargs)
	cmd, err := remoteAnnexCommand(annexbinpath, gitdir, annexargs...)
	if err != nil {
		return "", "", err
	}
	stdout, stderr, err := cmd.OutputError()

	return string(stdout), string(stderr), err
}

// annexAvailable checks whether annex is available to the gin client library.
// The function returns false with no error, if the annex command execution
// ends with the git message that 'annex' is not a git command.
// It will return false and the error message on any different error.
func annexAvailable(annexbinpath string, gitdir string) (bool, error) {
	_, stderr, err := annexCMD(annexbinpath, gitdir, "version")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

func main() {
	fmt.Println("Checking if annex is available")

	annexpath := ""
	repopath := ""

	// check if annex is available; exit otherwise
	ok, err := annexAvailable(annexpath, repopath)
	if err != nil {
		fmt.Printf("[E] checking annex: %s", err.Error())
		os.Exit(1)
	}

	if !ok {
		fmt.Printf("[E] Annex is not available at %s", annexpath)
		os.Exit(1)
	}
}
