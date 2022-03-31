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

// annexCommand sets up a git annex command with the provided arguments and returns a ShellCmd struct.
func annexCommand(annexbinpath string, gitdir string, cmdargs ...string) (ShellCmd, error) {
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
	cmd := shellCommand("git", cmdstr...)

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
	_, stderr, err := versatileGitCommand("", true, "", "version")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

// prevAnnexAvailable checks whether annex is available to the gin client library.
// The function returns false with no error, if the annex command execution
// ends with the git message that 'annex' is not a git command.
// It will return false and the error message on any different error.
func prevAnnexAvailable(annexbinpath string) (bool, error) {
	_, stderr, err := annexCMD(annexbinpath, "", "version")
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
	stdout, stderr, err := annexCMD(annexbinpath, repopath, "findref", "HEAD", "--not", "--in=here")
	if err != nil {
		return ai, err
	}

	fmt.Printf("[I] %q, %q\n", stdout, stderr)

	return ai, nil
}
