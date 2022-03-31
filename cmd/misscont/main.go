package main

import (
	"fmt"

	"github.com/spf13/cobra"
)

const appversion = "v0.0.2"

func setUpCommands(verstr string) *cobra.Command {
	var rootCmd = &cobra.Command{
		Use:                   "misscont",
		Long:                  "Collect missing annex content and git repository information (recursively)",
		Version:               fmt.Sprintln(verstr),
		DisableFlagsInUseLine: true,
	}
	cmds := make([]*cobra.Command, 1)
	cmds[0] = &cobra.Command{
		Use:                   "repoinfo",
		Short:                 "Collect git repository information",
		Args:                  cobra.NoArgs,
		Run:                   repoinfocmd,
		Version:               verstr,
		DisableFlagsInUseLine: true,
	}
	cmds[0].Flags().StringP("rootdir", "d", "", "Starting directory to recursively walk through a directory tree and collect git and annex repository information")

	rootCmd.AddCommand(cmds...)
	return rootCmd
}

// main checks git annex availability and runs the git annex repo statistics with the provided directory tree.
// TODO not sure how to best handle annex; currently it expects the binary to be in the same directory as the
// annex content directory; in any case, the user running the binary has to have a home directory for annex to
// use the [home]/.cache directory.
func main() {
	verstr := fmt.Sprintf("misscont %s", appversion)

	rootCmd := setUpCommands(verstr)
	rootCmd.SetVersionTemplate("{{.Version}}")

	err := rootCmd.Execute()
	if err != nil {
		fmt.Printf("[E] running misscont: %q\n", err.Error())
	}
}
