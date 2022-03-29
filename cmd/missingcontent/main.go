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
