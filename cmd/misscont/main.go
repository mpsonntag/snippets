package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
)

const appversion = "v0.0.1"

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
	_, stderr, err := annexCMD(annexbinpath, "", "version")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			return false, nil
		}
		return false, fmt.Errorf("%s, %s", stderr, err.Error())
	}
	return true, nil
}

func setUpCommands(verstr string) *cobra.Command {
	var rootCmd = &cobra.Command{
		Use:                   "misscont",
		Long:                  "Indentify missing annex content (recursively)",
		Version:               fmt.Sprintln(verstr),
		DisableFlagsInUseLine: true,
	}
	cmds := make([]*cobra.Command, 1)
	cmds[0] = &cobra.Command{
		Use:                   "start",
		Short:                 "Run the missing annex content check",
		Args:                  cobra.NoArgs,
		Run:                   checkgitdirs,
		Version:               verstr,
		DisableFlagsInUseLine: true,
	}
	cmds[0].Flags().StringP("checkdir", "d", "", "Starting directory to recursively walk through a directory tree and check git annex directories for missing content")

	rootCmd.AddCommand(cmds...)
	return rootCmd
}

func walkgitdirs(dirpath string) error {
	// check if the current directory is a git directory, bare or otherwise
	// assume the current directory is a bare git repo. stop and do all check stuff required
	if strings.HasSuffix(dirpath, ".git") {
		fmt.Printf("[I] current dir %q is a bare repo\n", dirpath)
		return nil
	}

	// check if the current directory is a normal git dir. stop and do all check stuff required
	checkgitpath := filepath.Join(dirpath, ".git")
	inf, err := os.Stat(checkgitpath)
	if err != nil && !os.IsNotExist(err) {
		fmt.Printf("[I] err checking git dir, will continue: %q\n", err.Error())
	} else if os.IsNotExist(err) {
		fmt.Println("[I] curr dir has no .git folder, moving on")
	} else if inf.IsDir() {
		fmt.Printf("[I] current dir %q is a git dir\n", dirpath)
		return nil
	}

	fmt.Printf("[I] curr dir %q is no git dir, continuing on\n", dirpath)
	return nil
}

func checkgitdirs(cmd *cobra.Command, args []string) {
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

	err = walkgitdirs(gitdirs)
	if err != nil {
		fmt.Printf("[E] walking directories: %s\n", err.Error())
	}
}

// main checks git annex availability and runs the git annex repo statistics with the provided directory tree.
// TODO not sure how to best handle annex; currently it expects the binary to be in the same directory as the
// annex content directory; in any case, the user running the binary has to have a home directory for annex to
// use the [home]/.cache directory.
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
		fmt.Printf("[E] annex is not available at %s\n", annexpath)
		os.Exit(1)
	}

	fmt.Println("[I] annex is available")

	verstr := fmt.Sprintf("misscont %s", appversion)

	rootCmd := setUpCommands(verstr)
	rootCmd.SetVersionTemplate("{{.Version}}")

	err = rootCmd.Execute()
	if err != nil {
		fmt.Printf("[E] running misscont: %q\n", err.Error())
	}
}
