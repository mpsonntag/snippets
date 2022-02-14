package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

// The gitCMD function messes up the directory paths; so lets
// not run the test for now
/* func TestGitCMD(t *testing.T) {
	targetpath, err := ioutil.TempDir("", "test_gitcmd")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(targetpath)

	// test non existing directory error
	_, _, err = gitCMD("/home/not/exist", "")
	if err == nil {
		t.Fatal("non existing directory should return an error")
	}

	// test non git directory error
	_, _, err = gitCMD(targetpath, "status")
	if err == nil {
		t.Fatal("non git directory should return an error")
	}

	// test valid git command
	_, _, err = gitCMD(targetpath, "init")
	if err != nil {
		t.Fatalf("error on initializing git dir: %q", err.Error())
	}
	_, stderr, err := gitCMD(targetpath, "status")
	if err != nil {
		t.Fatal("error on running git command")
	} else if stderr != "" {
		t.Fatalf("command error running git command: %q", stderr)
	}
}
 */

 func TestLocalAnnexCommand(t *testing.T) {
	targetpath, err := ioutil.TempDir("", "test_gitcmd")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(targetpath)

	// check annex is available to the test; stop the test otherwise
	stdout, stderr, err := annexRemoteCMD(targetpath, "info")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			t.Skipf("Annex is not available, skipping test...\n")
		}
		t.Fatalf("Failed to run test: %q, %q, %q", stdout, stderr, err.Error())
	}

	cmd := LocalAnnexCommand("find", "--not", "--in=here")
	stdoutb, stderrb, err := cmd.OutputError()
	fmt.Printf("%q. %q, %q", err.Error(), stdoutb, stderrb)
}

func TestMissingAnnexContent(t *testing.T) {
	targetpath, err := ioutil.TempDir("", "test_gitcmd")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(targetpath)

	// we could use that as well...
	// t.TempDir()

	// check annex is available to the test; stop the test otherwise
	stdout, stderr, err := annexRemoteCMD(targetpath, "info")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			t.Skipf("Annex is not available, skipping test...\n")
		}
		t.Fatalf("Failed to run test: %q, %q, %q", stdout, stderr, err.Error())
	}

	// test non existing directory error
	fmt.Println("Test non exist dir")
	_, _, err = missingAnnexContent("/home/not/exist")
	if err == nil {
		t.Fatal("non existing directory should return an error")
	}

	// test non git directory error
	fmt.Println("Test non git dir")
	stdout, stderr, err = missingAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git directory should return an error\n%s\n%s", stdout, stderr)
	}

	// initialize git directory
	fmt.Println("Init git dir")
	stdout, stderr, err = gitRemoteCMD(targetpath, "-C", targetpath, "init")
	if err != nil {
		t.Fatalf("could not initialize git repo: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git non annex dir error
	fmt.Println("Test non annex dir")
	stdout, stderr, err = missingAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git directory should return an error\n%s\n%s", stdout, stderr)
	}

	// initialize annex
	fmt.Println("Init annex")
	stdout, stderr, err = initAnnexForNow(targetpath)
	if err != nil {
		t.Fatalf("could not init annex: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git annex dir no error
	fmt.Println("Test non annex dir")
	stdout, stderr, err = missingAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("git annex directory should not return an error\n%s\n%s", stdout, stderr)
	}

	fmt.Println("Test annex info")
	stdout, stderr, err = someRemoteAnnex(targetpath, "info")
	if err != nil {
		t.Fatalf("git annex directory should not return an error\n%s\n%s", stdout, stderr)
	}
	fmt.Printf("%q, %q\n", stderr, stdout)
}

 func TestGitRemoteCMD(t *testing.T) {
	targetpath, err := ioutil.TempDir("", "test_gitcmd")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(targetpath)

	// check annex is available to the test; stop the test otherwise
	stdout, stderr, err := annexRemoteCMD(targetpath, "info")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			t.Skipf("Annex is not available, skipping test...\n")
		}
		t.Fatalf("Failed to run test: %q, %q, %q", stdout, stderr, err.Error())
	}

	// test non existing directory error
	_, _, err = gitRemoteCMD("/home/not/exist", "-C", "/home/not/exist", "")
	if err == nil {
		t.Fatal("non existing directory should return an error")
	}

	// test non git directory error
	stdout, stderr, err = gitRemoteCMD(targetpath, "-C", targetpath, "status")
	if err == nil {
		t.Fatalf("non git directory should return an error\n%s\n%s", stdout, stderr)
	}

	// test valid git command
	stdout, stderr, err = gitRemoteCMD(targetpath, "-C", targetpath, "init")
	if err != nil {
		t.Fatalf("error on initializing git dir: %q, %q, %q", err.Error(), stdout, stderr)
	}
	stdout, stderr, err = gitRemoteCMD(targetpath, "-C", targetpath, "status")
	if err != nil {
		t.Fatalf("error on running git command: %q\n%s\n%s", err.Error(), stderr, stdout)
	} else if stderr != "" {
		t.Fatalf("command error running git command: %q", stderr)
	}
}

func TestRunannexcheck(t *testing.T) {
	targetpath, err := ioutil.TempDir("", "test_runannexcheck")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(targetpath)

	// check annex is available to the test; stop the test otherwise
	stdout, stderr, err := annexRemoteCMD(targetpath, "info")
	if err != nil {
		if strings.Contains(stderr, "'annex' is not a git command") {
			t.Skipf("Annex is not available, skipping test...\n")
		}
		t.Fatalf("Failed to run test: %q, %q, %q", stdout, stderr, err.Error())
	}

	// we are playing around with os paths here which can get nasty.
	// add full tests for directory switching to ensure the server
	// will not get confused

	// check curr dir
	//currdir, err := os.Getwd()
	//if err != nil {
	// change to path of the executable if possible and check again
	//path, err := os.Executable()
	//fmt.Printf("Executable path: %s", path)
	//if err != nil {
	//	t.Fatalf("Could not assert executable path: %s, %s", err.Error(), path)
	//	}
	//		err = os.Chdir(path)
	//		if err != nil {
	//t.Fatalf("Path issues arose: %s", err.Error())
	//		}
	//	}
	//currdir, err = os.Getwd()
	//if err != nil {
	//t.Fatalf("still issues with curr dir: %s", err.Error())
	//}
	//fmt.Printf("current dir A: %q\n", currdir)

	// test non existing directory
	repodir := "/home/not/exist"
	out, err := runannexcheckOld(repodir)
	fmt.Printf("Running non existing dir check: %q, %q", out, err.Error())
	if err == nil || !strings.Contains(err.Error(), "path not found") {
		// check directory after function
		t.Fatalf("missing error on invalid dir path: %q\n%s", out, err.Error())
	}

	// test non-git dir
	_, err = runannexcheckOld(targetpath)
	fmt.Printf("Running non existing dir check: %q", err.Error())
	if err == nil {
		t.Fatalf("missing error on non-git dir: %q\n%s", out, err.Error())
	}
	currdir, direrr := os.Getwd()
	if direrr != nil {
		t.Fatalf("Could not assert current directory: %s", direrr.Error())
	}
	fmt.Printf("current dir B: %q\n", currdir)

	// test non-git annex dir

	// test valid git, missing annex content

	// test valid git, locked annex content

	// test valid git, no annex content

	// test valid git, valid annex content
}
