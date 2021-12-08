package main

import (
	"fmt"

	"github.com/spf13/cobra"
)

var (
	appversion string
	build      string
	commit     string
)

func init() {
	if appversion == "" {
		appversion = "[dev]"
	}
}

func setUpCommands(verstr string) *cobra.Command {
	var rootCmd = &cobra.Command{
		Use:                   "tickexp",
		Long:                  "tickexp",
		Version:               fmt.Sprintln(verstr),
		DisableFlagsInUseLine: true,
	}
	cmds := make([]*cobra.Command, 1)
	cmds[0] = &cobra.Command{
		Use:                   "start",
		Short:                 "Start the tickexp service",
		Args:                  cobra.NoArgs,
		Run:                   tempFunc,
		Version:               verstr,
		DisableFlagsInUseLine: true,
	}

	rootCmd.AddCommand(cmds...)
	return rootCmd
}

func tempFunc() {
    fmt.Printf("Placeholder")
}

func main() {
	verstr := fmt.Sprintf("tickexp %s Build %s (%s)", appversion, build, commit)

	rootCmd := setUpCommands(verstr)
	rootCmd.SetVersionTemplate("{{.Version}}")

	// Engage
	err := rootCmd.Execute()
	if err != nil {
		fmt.Printf("Error running tickexp: %q\n", err.Error())
	}
}
