package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

/*
targetpath, err := ioutil.TempDir("", "test_gitcmd")
if err != nil {
	t.Fatalf("Failed to create temp directory: %v", err)
}
defer os.RemoveAll(targetpath)
*/

func TestRemoteGitCMD(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	targetpath := t.TempDir()

	// check running git command from non existing path
	_, _, err = remoteGitCMD("/I/do/no/exist", false, "version")
	if err == nil {
		t.Fatal("expected error on non existing directory")
	} else if !strings.Contains(err.Error(), "") {
		t.Fatalf("expected path not found error but got %q", err.Error())
	}

	// check running git command
	stdout, stderr, err := remoteGitCMD(targetpath, false, "version")
	if err != nil {
		t.Fatalf("%q, %q, %q", err.Error(), stderr, stdout)
	}
	// check running git annex command
	stdout, stderr, err = remoteGitCMD(targetpath, true, "version")
	if err != nil {
		t.Fatalf("%q, %q, %q", err.Error(), stderr, stdout)
	}
}

func TestMissingAnnexContent(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	targetpath := t.TempDir()

	// test non existing directory error
	_, _, err = missingAnnexContent("/home/not/exist")
	if err == nil {
		t.Fatal("non existing directory should return an error")
	}

	// test non git directory error
	ismissing, misslist, err := missingAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git directory should return an error\nmissing: %t\n%q", ismissing, misslist)
	}

	// initialize git directory
	stdout, stderr, err := remoteGitCMD(targetpath, false, "init")
	if err != nil {
		t.Fatalf("could not initialize git repo: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git non annex dir error
	ismissing, misslist, err = missingAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git annex directory should return an error\nmissing: %t\n%q", ismissing, misslist)
	}

	// initialize annex
	stdout, stderr, err = remoteGitCMD(targetpath, true, "init")
	if err != nil {
		t.Fatalf("could not init annex: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git annex dir no error
	ismissing, misslist, err = missingAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("git annex directory should not return an error\n%s\n%s\n%t", err.Error(), misslist, ismissing)
	}

	// check no missing annex files status
	// create annex data file
	fname := "datafile.txt"
	fpath := filepath.Join(targetpath, fname)
	err = ioutil.WriteFile(fpath, []byte("some data"), 0777)
	if err != nil {
		t.Fatalf("Error creating annex data file %q", err.Error())
	}
	// add file to the annex
	stdout, stderr, err = remoteGitCMD(targetpath, true, "add", fpath)
	if err != nil {
		t.Fatalf("error on git annex add file\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}
	// uninit annex file so the cleanup can happen but ignore any further issues
	// the temp folder will get cleaned up eventually anyway.
	defer remoteGitCMD(targetpath, true, "uninit", fpath)

	stdout, stderr, err = remoteGitCMD(targetpath, false, "commit", "-m", "'add annex file'")
	if err != nil {
		t.Fatalf("error on git commit file\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}
	// check no missing annex content
	ismissing, misslist, err = missingAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("missing annex content check should not return any issue\n%s\n%s\nmissing %t", err.Error(), misslist, ismissing)
	} else if ismissing || misslist != "" {
		t.Fatalf("unexpected missing content found: %t, %q", ismissing, misslist)
	}

	// drop annex file content; use --force since the file content is in no other annex repo and annex thoughtfully complains
	stdout, stderr, err = remoteGitCMD(targetpath, true, "drop", "--force", fpath)
	if err != nil {
		t.Fatalf("error on git annex drop content\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}

	// check missing annex content
	ismissing, misslist, err = missingAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("missing annex content check should not return any issue\n%s\n%t\n%s", err.Error(), ismissing, misslist)
	} else if !ismissing || misslist == "" {
		t.Fatalf("missing annex content check should return missing files\n%t\n%s\n", ismissing, misslist)
	} else if !strings.Contains(misslist, fname) {
		t.Fatalf("missing annex content did not identify missing content: %t %q", ismissing, misslist)
	}
}

func TestLockedAnnexContent(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	targetpath := t.TempDir()

	// test non existing directory error
	islocked, locklist, err := lockedAnnexContent("/home/not/exist")
	if err == nil {
		t.Fatalf("non existing directory should return an error (locked %t) %q", islocked, locklist)
	} else if islocked || locklist != "" {
		t.Fatalf("unexpected locked files (locked %t) %q", islocked, locklist)
	}

	// test non git directory error
	islocked, locklist, err = lockedAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git directory should return an error (locked %t) %q", islocked, locklist)
	} else if islocked || locklist != "" {
		t.Fatalf("unexpected locked files (locked %t) %q", islocked, locklist)
	}

	// initialize git directory
	stdout, stderr, err := remoteGitCMD(targetpath, false, "init")
	if err != nil {
		t.Fatalf("could not initialize git repo: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git non annex dir error
	islocked, locklist, err = lockedAnnexContent(targetpath)
	if err == nil {
		t.Fatalf("non git annex directory should return an error (locked %t) %q", islocked, locklist)
	} else if islocked || locklist != "" {
		t.Fatalf("unexpected locked files (locked %t) %q", islocked, locklist)
	}

	// initialize annex
	stdout, stderr, err = remoteGitCMD(targetpath, true, "init")
	if err != nil {
		t.Fatalf("could not init annex: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git annex dir no error on empty directory
	islocked, locklist, err = lockedAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("git annex directory should not return an error (locked %t) %s\n%s", islocked, locklist, err.Error())
	} else if islocked || locklist != "" {
		t.Fatalf("unexpected locked files (locked %t) %q", islocked, locklist)
	}

	// check no locked annex files status
	// create annex data file
	fname := "datafile.txt"
	fpath := filepath.Join(targetpath, fname)
	err = ioutil.WriteFile(fpath, []byte("some data"), 0777)
	if err != nil {
		t.Fatalf("Error creating annex data file %q", err.Error())
	}
	// add file to the annex; note that this will also lock the file by annex default
	stdout, stderr, err = remoteGitCMD(targetpath, true, "add", fpath)
	if err != nil {
		t.Fatalf("error on git annex add file\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}
	// uninit annex file so the cleanup can happen but ignore any further issues
	// the temp folder will get cleaned up eventually anyway.
	defer remoteGitCMD(targetpath, true, "uninit", fpath)

	// check no locked annex content
	islocked, locklist, err = lockedAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("locked annex content check should not return any issue (locked %t) %s\n%s", islocked, locklist, err.Error())
	} else if !islocked || locklist == "" {
		t.Fatalf("unexpected unlocked content (locked %t) %q", islocked, locklist)
	} else if !strings.Contains(locklist, fname) {
		t.Fatalf("locked annex content did not identify locked content: %t %q", islocked, locklist)
	}

	// unlock annex file content
	stdout, stderr, err = remoteGitCMD(targetpath, true, "unlock", fpath)
	if err != nil {
		t.Fatalf("error on git annex lock content\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}

	// check unlocked annex content
	islocked, locklist, err = lockedAnnexContent(targetpath)
	if err != nil {
		t.Fatalf("unlocked annex content check should not return any issue (locked %t) %s\n%s", islocked, locklist, err.Error())
	} else if islocked || locklist != "" {
		t.Fatalf("unexpected locked content (locked %t) %q", islocked, locklist)
	}
}

func TestAnnexContentCheck(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	// check silence on missing directory
	err = annexContentCheck("/i/do/not/exist")
	if err != nil {
		t.Fatalf("invalid dir should fail silently %q", err.Error())
	}

	targetpath := t.TempDir()

	// initialize git directory
	stdout, stderr, err := remoteGitCMD(targetpath, false, "init")
	if err != nil {
		t.Fatalf("could not initialize git repo: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// initialize annex
	stdout, stderr, err = remoteGitCMD(targetpath, true, "init")
	if err != nil {
		t.Fatalf("could not init annex: %q, %q, %q", err.Error(), stdout, stderr)
	}

	// test git annex dir no error on empty directory
	err = annexContentCheck(targetpath)
	if err != nil {
		t.Fatalf("empty dir should not return an error %q", err.Error())
	}

	// create annex data file
	fname := "datafile.txt"
	fpath := filepath.Join(targetpath, fname)
	err = ioutil.WriteFile(fpath, []byte("some data"), 0777)
	if err != nil {
		t.Fatalf("Error creating annex data file %q", err.Error())
	}
	// add file to the annex; note that this will also lock the file by annex default
	stdout, stderr, err = remoteGitCMD(targetpath, true, "add", fpath)
	if err != nil {
		t.Fatalf("error on git annex add file\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}
	// uninit annex file so the cleanup can happen but ignore any further issues
	// the temp folder will get cleaned up eventually anyway.
	defer remoteGitCMD(targetpath, true, "uninit", fpath)

	// check error on locked file
	err = annexContentCheck(targetpath)
	if err == nil {
		t.Fatal("expected error on locked file")
	} else if !strings.Contains(err.Error(), "found locked content in 1 files") {
		t.Fatalf("expected locked content message but got %q", err.Error())
	}

	// unlock annex file content
	stdout, stderr, err = remoteGitCMD(targetpath, true, "unlock", fpath)
	if err != nil {
		t.Fatalf("error on git annex lock content\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}

	// check no error
	err = annexContentCheck(targetpath)
	if err != nil {
		t.Fatalf("unexpected error %q", err.Error())
	}

	// check error on missing file content
	// drop annex file content; use --force since the file content is in no other annex repo and annex thoughtfully complains
	stdout, stderr, err = remoteGitCMD(targetpath, true, "drop", "--force", fpath)
	if err != nil {
		t.Fatalf("error on git annex drop content\n%s\n%s\n%s", err.Error(), stdout, stderr)
	}
	err = annexContentCheck(targetpath)
	if err == nil {
		t.Fatal("expected error on missing file content")
	} else if !strings.Contains(err.Error(), "found missing content in 1 files") {
		t.Fatalf("expected missing content message but got %q", err.Error())
	}
}

func TestGitRemoteCMD(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	targetpath := t.TempDir()

	// test non existing directory error
	_, _, err = remoteGitCMD("/home/not/exist", false, "version")
	if err == nil {
		t.Fatal("non existing directory should return an error")
	}

	// test non git directory error
	stdout, stderr, err := remoteGitCMD(targetpath, false, "status")
	if err == nil {
		t.Fatalf("non git directory should return an error\n%s\n%s", stdout, stderr)
	}

	// test valid git command
	stdout, stderr, err = remoteGitCMD(targetpath, false, "init")
	if err != nil {
		t.Fatalf("error on initializing git dir: %q, %q, %q", err.Error(), stdout, stderr)
	}
	stdout, stderr, err = remoteGitCMD(targetpath, false, "status")
	if err != nil {
		t.Fatalf("error on running git command: %q\n%s\n%s", err.Error(), stderr, stdout)
	} else if stderr != "" {
		t.Fatalf("command error running git command: %q", stderr)
	}
}

func TestRunannexcheck(t *testing.T) {
	// check annex is available to the test; stop the test otherwise
	hasAnnex, err := annexAvailable()
	if err != nil {
		t.Fatalf("Error checking git annex: %q", err.Error())
	} else if !hasAnnex {
		t.Skipf("Annex is not available, skipping test...\n")
	}

	targetpath := t.TempDir()

	// test non existing directory
	repodir := "/home/not/exist"
	out, err := runannexcheck(repodir)
	fmt.Printf("Running non existing dir check: %q, %q", out, err.Error())
	if err == nil || !strings.Contains(err.Error(), "path not found") {
		// check directory after function
		t.Fatalf("missing error on invalid dir path: %q\n%s", out, err.Error())
	}

	// test non-git dir
	_, err = runannexcheck(targetpath)
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
