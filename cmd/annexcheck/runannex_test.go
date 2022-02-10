package main

import (
	"io/ioutil"
	"os"
	"testing"
)

func TestGitCMD(t *testing.T) {
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
