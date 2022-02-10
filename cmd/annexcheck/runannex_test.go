package main

import (
	"testing"
)

func TestSimpleRun(t *testing.T) {
	repodir := "/home/sommer/Chaos/DL/annextmp"
	_, _, err := runannexcheck(repodir)
	if err != nil {
		t.Fatalf("I think we got something: %s", err.Error())
	}
}
