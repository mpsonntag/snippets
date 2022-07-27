package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/user"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/G-Node/gin-cli/ginclient"
	gingit "github.com/G-Node/gin-cli/git"
	"github.com/G-Node/gin-cli/git/shell"
	"github.com/G-Node/gin-valid/internal/log"
	humanize "github.com/dustin/go-humanize"
)

type localginerror = shell.Error

func localGitConfigSet(gitdir, key, value string) error {
	log.ShowWrite("[Info] setting git config %q: %q at %q", key, value, gitdir)
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		return fmt.Errorf("[Error] gitdir %q not found", gitdir)
	} else if !isGitRepo(gitdir) {
		return fmt.Errorf("[Error] %q is not a git repository", gitdir)
	}

	// hijack default gin command environment for remote gitdir execution
	cmd := gingit.Command("config", "--local", key, value)
	cmd.Args = []string{"git", "-C", gitdir, "config", "--local", key, value}
	stdout, stderr, err := cmd.OutputError()
	if err != nil {
		fn := fmt.Sprintf("ConfigSet(%s, %s)", key, value)
		gerr := localginerror{UError: string(stderr), Origin: fn}
		log.ShowWrite("[Error] git config set; out: %s; err: %s", string(stdout), string(stderr))
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

// localExpandglobs expands a list of globs into paths (files and directories).
// If strictmatch is true, an error is returned if at least one element of the input slice does not match a real path,
// otherwise the pattern itself is returned when it matches no existing path.
func localExpandglobs(paths []string, strictmatch bool) (globexppaths []string, err error) {
	if len(paths) == 0 {
		// Nothing to do
		globexppaths = paths
		return
	}
	// expand potential globs
	for _, p := range paths {
		log.Write("ExpandGlobs: Checking for glob expansion for %s", p)
		exp, globerr := filepath.Glob(p)
		if globerr != nil {
			log.Write(globerr.Error())
			log.Write("Bad file pattern %s", p)
			return nil, globerr
		}
		if exp == nil {
			log.Write("ExpandGlobs: No files matched")
			if strictmatch {
				return nil, fmt.Errorf("no files matched %v", p)
			}
			exp = []string{p}
		}
		globexppaths = append(globexppaths, exp...)
	}
	return
}

// remoteGetContent downloads the contents of placeholder files in a checked out repository.
// The status channel 'getcontchan' is closed when this function returns.
// The git annex command is run in a provided directory and not the current one.
func remoteGetContent(remoteGitDir string, paths []string, getcontchan chan<- gingit.RepoFileStatus, rawMode bool) {
	defer close(getcontchan)
	log.ShowWrite("[Info] remoteGetContent")

	paths, err := localExpandglobs(paths, true)

	if err != nil {
		getcontchan <- gingit.RepoFileStatus{Err: err}
		return
	}

	annexgetchan := make(chan gingit.RepoFileStatus)
	go remoteAnnexGet(remoteGitDir, paths, annexgetchan, rawMode)
	for stat := range annexgetchan {
		getcontchan <- stat
	}
}

// remoteCloneRepo clones a remote repository and initialises annex.
// The status channel 'clonechan' is closed when this function returns.
func remoteCloneRepo(gincl *ginclient.Client, repopath, clonedir string, clonechan chan<- gingit.RepoFileStatus) {
	defer close(clonechan)
	log.ShowWrite("[Info] starting remoteCloneRepo")
	clonestatus := make(chan gingit.RepoFileStatus)
	remotepath := fmt.Sprintf("%s/%s", gincl.GitAddress(), repopath)
	go remoteClone(remotepath, repopath, clonedir, clonestatus)
	for stat := range clonestatus {
		clonechan <- stat
		if stat.Err != nil {
			return
		}
	}

	repoPathParts := strings.SplitN(repopath, "/", 2)
	repoName := repoPathParts[1]
	gitdir := filepath.Join(clonedir, repoName)

	status := gingit.RepoFileStatus{State: "Initialising local storage"}
	clonechan <- status
	// os.Chdir(repoName)
	err := remoteInitDir(gincl, gitdir)
	if err != nil {
		status.Err = err
		clonechan <- status
		return
	}
	status.Progress = "100%"
	clonechan <- status
	return
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

// remoteInitDir initialises the local directory with the default
// remote and git (and annex) configuration options.
func remoteInitDir(gincl *ginclient.Client, gitdir string) error {
	initerr := localginerror{Origin: "InitDir", Description: "Error initialising local directory"}

	// check if the provided directory is a git directory
	if !isGitRepo(gitdir) {
		return fmt.Errorf("[Error] provided path is not a git directory: %q", gitdir)
	}

	remoteInitConfig(gincl, gitdir)

	hostname, err := os.Hostname()
	if err != nil {
		hostname = "(unknownhost)"
	}
	description := fmt.Sprintf("%s@%s", gincl.Username, hostname)
	err = remoteAnnexInit(gitdir, description)
	if err != nil {
		initerr.UError = err.Error()
		return initerr
	}

	return nil
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

// remoteAnnexGet retrieves the content of specified files.
// The status channel 'getchan' is closed when this function returns.
// (git annex get)
func remoteAnnexGet(gitdir string, filepaths []string, getchan chan<- gingit.RepoFileStatus, rawMode bool) {
	defer close(getchan)
	log.ShowWrite("[Info] remoteAnnexGet")
	if _, err := os.Stat(gitdir); os.IsNotExist(err) {
		log.ShowWrite("[Warning] remoteAnnexGet path not found %q", gitdir)
		return
	}

	cmdargs := []string{"git", "-C", gitdir, "annex", "get"}
	if !rawMode {
		cmdargs = append(cmdargs, "--json-progress")
	}
	cmdargs = append(cmdargs, filepaths...)
	cmd := gingit.AnnexCommand("version")
	cmd.Args = cmdargs
	log.ShowWrite("[Info] remoteAnnexGet: %v", cmdargs)
	if err := cmd.Start(); err != nil {
		getchan <- gingit.RepoFileStatus{Err: err}
		return
	}

	var status gingit.RepoFileStatus
	status.State = "Downloading"

	var outline []byte
	var rerr error
	var progress localAnnexProgress
	var getresult localAnnexAction
	var prevByteProgress int
	var prevT time.Time

	for rerr = nil; rerr == nil; outline, rerr = cmd.OutReader.ReadBytes('\n') {
		if len(outline) == 0 {
			// skip empty lines
			continue
		}

		if rawMode {
			lineInput := cmd.Args
			input := strings.Join(lineInput, " ")
			status.RawInput = input
			status.RawOutput = string(outline)
			getchan <- status
			continue
		}

		err := json.Unmarshal(outline, &progress)
		if err != nil || progress.Action.Command == "" {
			// File done? Check if succeeded and continue to next line
			err = json.Unmarshal(outline, &getresult)
			if err != nil || getresult.Command == "" {
				// Couldn't parse output
				log.ShowWrite("[Warning] Could not parse 'git annex get' output")
				log.ShowWrite(string(outline))
				// TODO: Print error at the end: Command succeeded but there was an error understanding the output
				continue
			}
			status.FileName = getresult.File
			if getresult.Success {
				status.Progress = "100%"
				status.Err = nil
			} else {
				errmsg := getresult.Note
				if strings.Contains(errmsg, "Unable to access") {
					errmsg = "authorisation failed or remote storage unavailable"
				}
				status.Err = fmt.Errorf("failed: %s", errmsg)
			}
		} else {
			status.FileName = progress.Action.File
			status.Progress = progress.PercentProgress
			dbytes := progress.ByteProgress - prevByteProgress
			now := time.Now()
			dt := now.Sub(prevT)
			status.Rate = localCalcRate(dbytes, dt)
			prevByteProgress = progress.ByteProgress
			prevT = now
			status.Err = nil
		}

		getchan <- status
	}
	if cmd.Wait() != nil {
		var stderr, errline []byte
		for rerr = nil; rerr == nil; errline, rerr = cmd.OutReader.ReadBytes('\000') {
			stderr = append(stderr, errline...)
		}
		log.ShowWrite("[Error] remoteAnnexGet: %s", string(stderr))
	}
}

func localCalcRate(dbytes int, dt time.Duration) string {
	dtns := dt.Nanoseconds()
	if dtns <= 0 || dbytes <= 0 {
		return ""
	}
	rate := int64(dbytes) * 1000000000 / dtns
	return fmt.Sprintf("%s/s", humanize.IBytes(uint64(rate)))
}

// Types (private)
type localAnnexAction struct {
	Command string   `json:"command"`
	Note    string   `json:"note"`
	Success bool     `json:"success"`
	Key     string   `json:"key"`
	File    string   `json:"file"`
	Errors  []string `json:"error-messages"`
}

type localAnnexProgress struct {
	Action          localAnnexAction `json:"action"`
	ByteProgress    int              `json:"byte-progress"`
	TotalSize       int              `json:"total-size"`
	PercentProgress string           `json:"percent-progress"`
}

func remoteGitCommitCheckout(gitdir, hash string) error {
	// add "isGitDir" check
	log.ShowWrite("[Info] checking out commit %q at %q", hash, gitdir)
	cmdargs := []string{"git", "-C", gitdir, "checkout", hash, "--"}
	cmd := gingit.Command("version")
	cmd.Args = cmdargs
	stdout, stderr, err := cmd.OutputError()
	if err != nil {
		log.ShowWrite("[Error] remoteGitCheckout: [stdout]\n%s\n[stderr]\n%s", string(stdout), string(stderr))
		return fmt.Errorf(string(stderr))
	}
	return nil
}

func main() {
	fmt.Println("...[I] running ginutils")
}
