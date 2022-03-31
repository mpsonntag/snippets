package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func versatileGitCommand(remotegitdir string, useannex bool, annexbinpath string, cmdargs ...string) (string, string, error) {
	fmt.Printf("[I] preparing cmd %v at path %q (annex at %q)\n", cmdargs, remotegitdir, annexbinpath)
	var cmdvarstr []string

	// check the provided path if the cmd is supposed to be run at a specific location
	if remotegitdir != "" {
		if _, err := os.Stat(remotegitdir); os.IsNotExist(err) {
			return "", "", fmt.Errorf("gitdir path not found %q", remotegitdir)
		}
		cmdvarstr = append(cmdvarstr, "-C", remotegitdir)
	}

	if useannex {
		cmdvarstr = append(cmdvarstr, "annex")
	}

	cmdvarstr = append(cmdvarstr, cmdargs...)
	cmd := shellCommand("git", cmdvarstr...)

	// add a provided local annex binary path to the command runtime environment
	if useannex && annexbinpath != "" {
		if _, err := os.Stat(annexbinpath); os.IsNotExist(err) {
			return "", "", fmt.Errorf("annex path not found %q", annexbinpath)
		}
		// --- more in depth annex path check

		env := os.Environ()
		syspath := os.Getenv("PATH")
		// --- refactor the next lines to use proper string formatting
		syspath += string(os.PathListSeparator) + annexbinpath
		cmd.Env = append(env, fmt.Sprintf("PATH=%s", syspath))
		// newenv := fmt.Sprintf("PATH=%s%s%s", syspath, string(os.PathListSeparator), annexbinpath)
		// cmd.Env = append(env, newenv)
	}

	workingdir, _ := filepath.Abs(".")
	fmt.Printf("[I] running shell cmd in %q (for %q): %q\n", workingdir, remotegitdir, strings.Join(cmd.Args, " "))

	stdout, stderr, err := cmd.OutputError()
	return string(stdout), string(stderr), err
}

// annexAvailable checks whether annex is available to the gin client library.
// The function returns false with no error, if the annex command execution
// ends with the git message that 'annex' is not a git command.
// It will return false and the error message on any different error.
// The optional annexbinpath can be used to provide a local annex binary if
// the host does not provide annex.
func annexAvailable(annexbinpath string) (bool, error) {
	_, stderr, err := versatileGitCommand("", true, annexbinpath, "version")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

func infoFromBareRepo(annexbinpath, repopath string) (AnnexInfo, error) {
	ai := AnnexInfo{}
	stdout, stderr, err := versatileGitCommand(repopath, true, annexbinpath, "findref", "HEAD", "--not", "--in=here")
	if err != nil {
		return ai, err
	}

	fmt.Printf("[I] %q, %q\n", stdout, stderr)

	return ai, nil
}
