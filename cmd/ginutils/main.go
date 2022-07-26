package main

import (
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

func main() {
	fmt.Println("...[I] running ginutils")
}
