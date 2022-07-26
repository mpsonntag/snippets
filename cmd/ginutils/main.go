package main

import (
	"bytes"
	"fmt"

	gingit "github.com/G-Node/gin-cli/git"
	"github.com/G-Node/gin-cli/git/shell"
	"github.com/G-Node/gin-valid/internal/log"
)

type localginerror = shell.Error

func localGitConfigSet(key, value, gitdir string) error {
	fn := fmt.Sprintf("ConfigSet(%s, %s)", key, value)

	// hijack command for remote gitdir execution
	cmd := gingit.Command("config", "--local", key, value)
	cmd.Args = []string{"git", "-C", gitdir, "config", "--local", key, value}
	stdout, stderr, err := cmd.OutputError()
	if err != nil {
		gerr := localginerror{UError: string(stderr), Origin: fn}
		log.ShowWrite("Error during config set")
		log.ShowWrite("[stdout]\n%s\n[stderr]\n%s", string(stdout), string(stderr))
		return gerr
	}
	return nil
}

func isGitRepo(path string) bool {
	cmd := gingit.Command("version")
	cmdargs := []string{"git", "-C", path, "rev-parse"}
	cmd.Args = cmdargs
	_, stderr, err := cmd.OutputError()
	if err != nil {
		log.ShowWrite("[Error] running git rev-parse: %s", err.Error())
		return false
	} else if bytes.Contains(stderr, []byte("not a git repository")) {
		return false
	}
	return true
}

func main() {
	fmt.Println("...[I] running ginutils")
}
