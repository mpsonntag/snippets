package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func versatileGitCommand(remotegitdir string, useannex bool, annexbinpath string, cmdargs ...string) (string, string, error) {
	fmt.Printf("[I] preparing command: %s, %s, %v\n", remotegitdir, annexbinpath, cmdargs)
	var cmdvarstr []string
	if remotegitdir != "" {
		if _, err := os.Stat(remotegitdir); os.IsNotExist(err) {
			return "", "", fmt.Errorf("gitdir path not found %q", remotegitdir)
		}
		cmdvarstr = append(cmdvarstr, "-C", remotegitdir)
	}

	if useannex {
		cmdvarstr = append(cmdvarstr, "annex")
		if _, err := os.Stat(annexbinpath); os.IsNotExist(err) {
			return "", "", fmt.Errorf("annex path not found %q", annexbinpath)
		}
		// todo ... more in depth annex path check
	}

	cmdvarstr = append(cmdvarstr, cmdargs...)
	cmd := shellCommand("git", cmdvarstr...)

	if useannex {
		// make sure the local annex is available to the command
		env := os.Environ()
		syspath := os.Getenv("PATH")
		syspath += string(os.PathListSeparator) + annexbinpath
		cmd.Env = append(env, fmt.Sprintf("PATH=%s", syspath))
	}

	workingdir, _ := filepath.Abs(".")
	fmt.Printf("[I] shell cmd in %q (for %q): %q\n", workingdir, remotegitdir, strings.Join(cmd.Args, " "))

	stdout, stderr, err := cmd.OutputError()
	return string(stdout), string(stderr), err
}

// annexAvailable checks whether annex is available to the gin client library.
// The function returns false with no error, if the annex command execution
// ends with the git message that 'annex' is not a git command.
// It will return false and the error message on any different error.
func annexAvailable(annexbinpath string) (bool, error) {
	_, stderr, err := versatileGitCommand("", true, "", "version")
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
