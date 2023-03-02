package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
)

// CommitListItem stores git commit information.
type CommitListItem struct {
	Commit    string `json:"commit"`
	Committer string `json:"committer"`
	Author    string `json:"author"`
	//Date       time.Time  `json:"date"`
	DateIso      string   `json:"date-iso"`
	DateRelative string   `json:"date-rel"`
	Subject      string   `json:"subject"`
	Changes      []string `json:"changes"`
}

func parseCommitList(repoPath string) {
	// execute log command for repo at repoPath
	usefmt := "--pretty=format:Commit:=%H%nCommitter:=%cn%nAuthor:=%an%nDate-iso:=%ai%nDate-rel:=%ar%nSubject:=%s%nChanges:="
	cmdStr := fmt.Sprintf("git -C %s log %s --name-status", repoPath, usefmt)
	fmt.Printf("Running command\n    %s\n", cmdStr)
	cmd := exec.Command(cmdStr)
	body, err := cmd.Output()
	if err != nil {
		fmt.Printf("Failed running git log: %v\n", err)
		return
	}
	var comList []CommitListItem
	r := bytes.NewReader(body)
	br := bufio.NewReader(r)

	var changesFlag bool

	for {
		// Consume line until newline character
		l, err := br.ReadString('\n')

		if strings.Contains(l, ":=") {
			splitList := strings.SplitN(l, ":=", 2)

			key := splitList[0]
			val := splitList[1]
			switch key {
			case "Commit":
				// reset non key line flags
				changesFlag = false
				newCommit := CommitListItem{Commit: val}
				comList = append(comList, newCommit)
			case "Committer":
				comList[len(comList)-1].Committer = val
			case "Author":
				comList[len(comList)-1].Author = val
			case "Date-iso":
				comList[len(comList)-1].DateIso = val
			case "Date-rel":
				comList[len(comList)-1].DateRelative = val
			case "Subject":
				comList[len(comList)-1].Subject = val
			case "Changes":
				// Setting changes flag so we know, that the next lines are probably file change notification lines.
				changesFlag = true
			default:
				fmt.Printf("Encountered unexpected key: '%s', value: '%s'\n", key, strings.Trim(val, "\n"))
			}

		} else if changesFlag && strings.Contains(l, "\t") {
			comList[len(comList)-1].Changes = append(comList[len(comList)-1].Changes, l)
		}

		// Breaks latest when EOF err is raised
		if err != nil {
			break
		}
	}

	if err != io.EOF && err != nil {
		fmt.Printf("Encountered error: %v\n", err)
		return
	}

	fmt.Printf("Done parsing. There where '%d' commits: %v\n", len(comList), comList)

	enc := json.NewEncoder(os.Stdout)
	err = enc.Encode(comList)
	if err != nil {
		fmt.Printf("Error encoding struct: %v\n", err)
	}
	//fmt.Printf("Done encoding. This is the result: '%v'\n", len(comList), comList)
}

func main() {
	repoPath := "/home/msonntag/Chaos/DL/tmp/test_remote_git/bla/"
	fmt.Printf("Parsing repo %q\n", repoPath)
	parseCommitList(repoPath)
}
