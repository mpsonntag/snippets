package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/G-Node/gin-cli/git/shell"
)

// annexCommand sets up a git annex command with the provided arguments and returns a GinCmd struct.
func annexCommand(annexbinpath string, gitdir string, cmdargs ...string) (shell.Cmd, error) {
	if _, err := os.Stat(annexbinpath); os.IsNotExist(err) {
		return ShellCmd{}, fmt.Errorf("annex path not found %q", annexbinpath)
	}
	if gitdir != "" {
		if _, err := os.Stat(gitdir); os.IsNotExist(err) {
			return ShellCmd{}, fmt.Errorf("gitdir path not found %q", gitdir)
		}
	}

	// handle if a command is directory dependent
	cmdvarstr := []string{"annex"}
	if gitdir != "" {
		cmdvarstr = []string{"-C", gitdir, "annex"}
	}
	cmdstr := append(cmdvarstr, cmdargs...)
	cmd := shell.Command("git", cmdstr...)

	// make sure the local annex is available to the command
	env := os.Environ()
	syspath := os.Getenv("PATH")
	syspath += string(os.PathListSeparator) + annexbinpath
	cmd.Env = append(env, fmt.Sprintf("PATH=%s", syspath))

	workingdir, _ := filepath.Abs(".")
	fmt.Printf("[I] shell cmd in %q (for %q): %q\n", workingdir, gitdir, strings.Join(cmd.Args, " "))

	return cmd, nil
}

// annexCMD runs the passed git annex command arguments.
// The command returns stdout and stderr as strings and any error that might occur.
func annexCMD(annexbinpath string, gitdir string, annexargs ...string) (string, string, error) {
	fmt.Printf("[I] running annex cmd: %s\n", annexargs)
	cmd, err := annexCommand(annexbinpath, gitdir, annexargs...)
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
func annexAvailable(annexbinpath string) (bool, error) {
	_, stderr, err := annexCMD(annexbinpath, "", "version")
	fmt.Printf("%q, %v\n", stderr, err)
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

func main() {
	binpath, err := os.Executable()
	if err != nil {
		fmt.Printf("[E] fetching executable path: %s\n", err.Error())
		os.Exit(1)
	}
	if _, err := os.Stat(binpath); os.IsNotExist(err) {
		fmt.Printf("[E] executable path could not be identified: %s\n", err.Error())
		os.Exit(1)
	}
	fmt.Printf("[I] using binpath at %q\n", binpath)

	binname := filepath.Base(binpath)
	annexpath := strings.Replace(binpath, binname, "git-annex.linux", 1)

	// annexpath := filepath.Join(binpath, "git-annex.linux")
	if _, err := os.Stat(annexpath); err != nil {
		fmt.Printf("[E] annex binary path not found: %s\n", err.Error())
		os.Exit(1)
	}
	fmt.Printf("[I] using annexpath %q\n", annexpath)

	// check if annex is available; exit otherwise
	ok, err := annexAvailable(annexpath)
	if err != nil {
		fmt.Printf("[E] checking annex: %s\n", err.Error())
		os.Exit(1)
	}

	if !ok {
		fmt.Printf("[E] Annex is not available at %s\n", annexpath)
		os.Exit(1)
	}

	fmt.Println("[I] annex is available")
}
