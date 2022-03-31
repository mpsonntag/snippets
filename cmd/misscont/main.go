package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

const appversion = "v0.0.1"

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

// main checks git annex availability and runs the git annex repo statistics with the provided directory tree.
// TODO not sure how to best handle annex; currently it expects the binary to be in the same directory as the
// annex content directory; in any case, the user running the binary has to have a home directory for annex to
// use the [home]/.cache directory.
func main() {
	annexpath, err := handlebinpath()
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
	fmt.Printf("[I] using available annex at %q\n", annexpath)

	verstr := fmt.Sprintf("misscont %s", appversion)

	rootCmd := setUpCommands(verstr)
	rootCmd.SetVersionTemplate("{{.Version}}")

	err = rootCmd.Execute()
	if err != nil {
		fmt.Printf("[E] running misscont: %q\n", err.Error())
	}
}
