package main

import (
	"bytes"
	"fmt"
	"os/user"
	"runtime"
	"strings"

	"github.com/G-Node/gin-cli/ginclient"
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

func localcutline(b []byte) (string, bool) {
	idx := -1
	cridx := bytes.IndexByte(b, '\r')
	nlidx := bytes.IndexByte(b, '\n')
	if cridx > 0 {
		idx = cridx
	} else {
		cridx = len(b) + 1
	}
	if nlidx > 0 && nlidx < cridx {
		idx = nlidx
	}
	if idx <= 0 {
		return string(b), true
	}
	return string(b[:idx]), false
}

func remoteClone(remotepath string, repopath string, clonedir string, clonechan chan<- gingit.RepoFileStatus) {
	// TODO: This function is crazy huge - simplify
	fn := fmt.Sprintf("Clone(%s)", remotepath)
	defer close(clonechan)
	args := []string{"clone", "--progress", remotepath}
	if runtime.GOOS == "windows" {
		// force disable symlinks even if user can create them
		// see https://git-annex.branchable.com/bugs/Symlink_support_on_Windows_10_Creators_Update_with_Developer_Mode/
		args = append([]string{"-c", "core.symlinks=false"}, args...)
	}
	// hijack gingit to execute command remotely
	cmd := gingit.Command(args...)
	cmdargs := []string{"git", "-C", clonedir}
	cmdargs = append(cmdargs, args...)
	cmd.Args = cmdargs
	err := cmd.Start()
	if err != nil {
		clonechan <- gingit.RepoFileStatus{Err: localginerror{UError: err.Error(), Origin: fn}}
		return
	}

	var line string
	var stderr []byte
	var status gingit.RepoFileStatus
	status.State = "Downloading repository"
	clonechan <- status
	var rerr error
	readbuffer := make([]byte, 1024)
	var nread, errhead int
	var eob, eof bool
	lineInput := cmd.Args
	input := strings.Join(lineInput, " ")
	status.RawInput = input
	// git clone progress prints to stderr
	for eof = false; !eof; nread, rerr = cmd.ErrReader.Read(readbuffer) {
		if rerr != nil && errhead == len(stderr) {
			eof = true
		}
		stderr = append(stderr, readbuffer[:nread]...)
		for eob = false; !eob || errhead < len(stderr); line, eob = localcutline(stderr[errhead:]) {
			if len(line) == 0 {
				errhead++
				break
			}
			errhead += len(line) + 1
			words := strings.Fields(line)
			status.FileName = repopath
			if strings.HasPrefix(line, "Receiving objects") {
				if len(words) > 2 {
					status.Progress = words[2]
				}
				if len(words) > 8 {
					rate := fmt.Sprintf("%s%s", words[7], words[8])
					if strings.HasSuffix(rate, ",") {
						rate = strings.TrimSuffix(rate, ",")
					}
					status.Rate = rate
					status.RawOutput = line
				}
			}
			clonechan <- status
		}
	}

	errstring := string(stderr)
	if err = cmd.Wait(); err != nil {
		log.Write("Error during clone command")
		repoPathParts := strings.SplitN(repopath, "/", 2)
		repoOwner := repoPathParts[0]
		repoName := repoPathParts[1]
		gerr := localginerror{UError: errstring, Origin: fn}
		if strings.Contains(errstring, "does not exist") {
			gerr.Description = fmt.Sprintf("Repository download failed\n"+
				"Make sure you typed the repository path correctly\n"+
				"Type 'gin repos %s' to see if the repository exists and if you have access to it",
				repoOwner)
		} else if strings.Contains(errstring, "already exists and is not an empty directory") {
			gerr.Description = fmt.Sprintf("Repository download failed.\n"+
				"'%s' already exists in the current directory and is not empty.", repoName)
		} else if strings.Contains(errstring, "Host key verification failed") {
			gerr.Description = "Server key does not match known/configured host key."
		} else {
			gerr.Description = fmt.Sprintf("Repository download failed. Internal git command returned: %s", errstring)
		}
		status.Err = gerr
		clonechan <- status
		// doesn't really need to break here, but let's not send the progcomplete
		return
	}
	// Progress doesn't show 100% if cloning an empty repository, so let's force it
	status.Progress = "100%"
	clonechan <- status
	return
}

// AnnexInit initialises the repository for annex.
// (git annex init)
func remoteAnnexInit(gitdir, description string) error {
	err := localGitConfigSet(gitdir, "annex.backends", "MD5")
	if err != nil {
		log.Write("Failed to set default annex backend MD5")
	}
	err = localGitConfigSet(gitdir, "annex.addunlocked", "true")
	if err != nil {
		log.Write("Failed to initialise annex in unlocked mode")
		return err
	}
	args := []string{"init", "--version=7", description}
	// hijack command for remote gitdir execution
	cmd := gingit.AnnexCommand(args...)
	cmdargs := []string{"git", "-C", gitdir, "annex"}
	cmdargs = append(cmdargs, args...)
	cmd.Args = cmdargs
	stdout, stderr, err := cmd.OutputError()
	if err != nil {
		initError := fmt.Errorf("Repository annex initialisation failed.\n%s", string(stderr))
		log.ShowWrite("[stdout]\n%s\n[stderr]\n%s", string(stdout), string(stderr))
		return initError
	}

	// hijack command for remote gitdir execution
	cmd = gingit.Command("checkout", "master")
	cmd.Args = []string{"git", "-C", gitdir, "checkout", "master"}
	stdout, stderr, err = cmd.OutputError()
	if err != nil {
		log.ShowWrite("[stdout]\n%s\n[stderr]\n%s", string(stdout), string(stderr))
	}

	return nil
}

func remoteInitConfig(gincl *ginclient.Client, gitdir string) {
	// If there is no git user.name or user.email set local ones
	cmd := gingit.Command("config", "user.name")
	cmdargs := []string{"git", "-C", gitdir, "config", "user.name"}
	cmd.Args = cmdargs
	globalGitName, _ := cmd.Output()
	if len(globalGitName) == 0 {
		info, ierr := gincl.RequestAccount(gincl.Username)
		name := info.FullName
		if ierr != nil || name == "" {
			name = gincl.Username
		}
		if name == "" {
			// gin user might not be logged in; fall back to system user
			u, _ := user.Current()
			name = u.Name
		}
		err := localGitConfigSet(gitdir, "user.name", name)
		if err != nil {
			log.ShowWrite("[Error] setting git config user.name: %s", err.Error())
		}
		err = localGitConfigSet(gitdir, "user.email", name)
		if err != nil {
			log.ShowWrite("[Error] setting git config user.email: %s", err.Error())
		}
	}
	// Disable quotepath: when enabled prints escape sequences for files with
	// unicode characters making it hard to work with, can break JSON
	// formatting, and sometimes impossible to reference specific files.
	err := localGitConfigSet(gitdir, "core.quotepath", "false")
	if err != nil {
		log.ShowWrite("[Error] setting git config core.quotepath: %s", err.Error())
	}
	if runtime.GOOS == "windows" {
		// force disable symlinks even if user can create them
		// see https://git-annex.branchable.com/bugs/Symlink_support_on_Windows_10_Creators_Update_with_Developer_Mode/
		err = localGitConfigSet(gitdir, "core.symlinks", "false")
		if err != nil {
			log.ShowWrite("[Error] setting git config core.symlinks: %s", err.Error())
		}
	}
}

func main() {
	fmt.Println("...[I] running ginutils")
}
