package main

import (
	"fmt"

	"github.com/spf13/cobra"
)

type gitrepoinfo struct {
	missingAnnex bool
	lockedAnnex bool
	annexSize int
	annexSizeUnit string
	gitSize int
	gitSizeUnit string
}

func runannexcheck() {
	fmt.Println("Running annexcheck")
}

func setUpCommands(verstr string) *cobra.Command {
	var rootCmd = &cobra.Command{
		Use:                   "annexcheck",
		Long:                  "annexcheck",
		Version:               fmt.Sprintln("0.0.1"),
		DisableFlagsInUseLine: true,
	}
	cmds := make([]*cobra.Command, 1)
	cmds[0] = &cobra.Command{
		Use:                   "run",
		Short:                 "run the annexcheck from the current directory",
		Args:                  cobra.NoArgs,
		Run:                   runannexcheck,
		Version:               fmt.Sprintln("0.0.1"),,
		DisableFlagsInUseLine: true,
	}

	rootCmd.AddCommand(cmds...)

	return rootCmd
}

func main() {
	fmt.Println("...[I] parsing CLI")

	err := rootCmd.Execute()
	if err != nil {
		fmt.Printf("...[E] running tickexp: %q\n", err.Error())
	}
}
