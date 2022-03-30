package main

import (
	"bufio"
	"bytes"
	"os/exec"
)

// ShellCmd/shellCommand are based on the Cmd implementation in github.com/G-Node/gin-cli/git/shell

// ShellCmd extends the exec.Cmd struct with convenience functions for reading piped
// output.
type ShellCmd struct {
	*exec.Cmd
	OutReader *bufio.Reader
	ErrReader *bufio.Reader
	Err       error
}

// shellCommand returns the ShellCmd struct to execute the named program with the
// given arguments.
func shellCommand(name string, args ...string) ShellCmd {
	cmd := exec.Command(name, args...)
	outpipe, _ := cmd.StdoutPipe()
	errpipe, _ := cmd.StderrPipe()
	outreader := bufio.NewReader(outpipe)
	errreader := bufio.NewReader(errpipe)

	return ShellCmd{cmd, outreader, errreader, nil}
}

// OutputError runs the command and returns the standard output and standard
// error as two byte slices.
func (cmd *ShellCmd) OutputError() ([]byte, []byte, error) {
	var bout, berr bytes.Buffer
	cmd.Stdout = &bout
	cmd.Stderr = &berr
	err := cmd.Run()
	return bout.Bytes(), berr.Bytes(), err
}
