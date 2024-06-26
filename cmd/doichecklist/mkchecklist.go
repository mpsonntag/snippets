package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/G-Node/libgin/libgin"
	"github.com/spf13/cobra"
	yaml "gopkg.in/yaml.v2"
)

// Default configuration struct containing non problematic test values
type checklist struct {
	// Entries required for every DOI request
	// Paste basic information from the corresponding issue on
	//   https://gin.g-node.org/G-Node/DOIMetadata
	// Automated registration [id] from "10.12751/g-node.[id]"
	Regid string `yaml:"reg_id"`
	// Repository owner
	Repoown string `yaml:"repo_own"`
	// Repository name
	Repo string `yaml:"repo"`
	// Date issued from doi.xml; Format YYYY-MM-DD
	Regdate string `yaml:"reg_date"`
	// DOI requestee email address
	Email string `yaml:"email"`
	// DOI requestee full name
	Userfullname string `yaml:"user_full_name"`
	// Entries that are usually handled automatically via repo datacite entry
	// DOI request title; usually handled automatically via repo datacite entry
	Title string `yaml:"title"`
	// Author citation list; usually handled automatically via repo datacite entry
	Citation string `yaml:"citation"`
	// Entries that are set once and remain unchanged for future DOI requests
	// User working on the DOI server
	Serveruser string `yaml:"server_user"`
	// Local staging dir to create index and keyword pages
	Dirlocalstage string `yaml:"dir_local_stage"`
	// Full ssh access name of the server hosting the GIN server instance
	Ginserver string `yaml:"gin_server"`
	// Full ssh access name of the server hosting the DOI server instance
	Doiserver string `yaml:"doi_server"`
	// DOI Server repo preparation directory
	Dirdoiprep string `yaml:"dir_doi_prep"`
	// DOI Server root doi hosting directory
	Dirdoi string `yaml:"dir_doi"`
}

// outFilename constructs a filename for the output markdown file
// from the checklist repo and registration information and
// returns it. Optionally an output path can be specified.
func outFilename(cl checklist, outpath string) string {
	owner := strings.ToLower(cl.Repoown)
	if len(cl.Repoown) > 5 {
		owner = owner[0:5]
	}
	reponame := strings.ToLower(cl.Repo)
	if len(cl.Repo) > 10 {
		reponame = reponame[0:15]
	}

	currdate := time.Now().Format("20060102")
	outfile := fmt.Sprintf("%s_%s-%s-%s.md", currdate, strings.ToLower(cl.Regid), owner, reponame)
	if outpath != "" {
		outfile = filepath.Join(outpath, outfile)
	}
	return outfile
}

// ChecklistTemplate is the data struct required to properly render
// the checklist file template.
type ChecklistTemplate struct {
	CL               checklist
	RepoLower        string
	RepoownLower     string
	SemiDOIScreenID  string
	FullDOIScreenID  string
	SemiDOICleanup   string
	SemiDOIDirpath   string
	FullDOIDirpath   string
	Forklog          string
	Logfiles         string
	Ziplog           string
	Zipfile          string
	KeywordsLocalDir string
	ToServer         string
	Citeyear         string
}

// mkchecklist creates an output markdown file with the contents
// of the passed checklist struct. A path for the output file can
// be provided.
func mkchecklist(cl checklist, outpath string) {
	outfile := outFilename(cl, outpath)

	fmt.Printf("-- Writing to checklist file %s\n", outfile)
	fip, err := os.Create(outfile)
	if err != nil {
		fmt.Printf("Could not create checklist file: %s\n", err.Error())
		return
	}
	defer fip.Close()

	tmpl, err := prepareTemplates("Checklist")
	if err != nil {
		fmt.Printf("Error preparing checklist template: %s", err.Error())
		return
	}

	fullcl := ChecklistTemplate{
		CL:               cl,
		RepoLower:        strings.ToLower(cl.Repo),
		RepoownLower:     strings.ToLower(cl.Repoown),
		SemiDOIScreenID:  fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randAlnum(5)),
		FullDOIScreenID:  fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randAlnum(5)),
		SemiDOICleanup:   fmt.Sprintf("%s/10.12751/g-node.%s", cl.Dirdoiprep, cl.Regid),
		SemiDOIDirpath:   fmt.Sprintf("%s/10.12751/g-node.%s/%s", cl.Dirdoiprep, cl.Regid, strings.ToLower(cl.Repo)),
		FullDOIDirpath:   fmt.Sprintf("%s/%s", cl.Dirdoiprep, strings.ToLower(cl.Repo)),
		Forklog:          fmt.Sprintf("%s-%s.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo)),
		Logfiles:         fmt.Sprintf("%s-%s*.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo)),
		Ziplog:           fmt.Sprintf("%s-%s_zip.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo)),
		Zipfile:          fmt.Sprintf("%s/10.12751/g-node.%s/10.12751_g-node.%s.zip", cl.Dirdoi, cl.Regid, cl.Regid),
		KeywordsLocalDir: fmt.Sprintf("%s/keywords", cl.Dirlocalstage),
		ToServer:         fmt.Sprintf("%s@%s:/home/%s/staging", cl.Serveruser, cl.Doiserver, cl.Serveruser),
		Citeyear:         time.Now().Format("2006"),
	}

	if err := tmpl.Execute(fip, fullcl); err != nil {
		fmt.Printf("Error writing checklist file: %s", err.Error())
		return
	}
	fmt.Printf("-- Finished writing checklist file %s\n", outfile)
}

// readChecklistConfigYAML parses config information from a provided yaml file and
// returns a checklist struct containing the config information.
func readChecklistConfigYAML(yamlInfo *checklist, confile string) (*checklist, error) {
	infoyml, err := readFileAtPath(confile)
	if err != nil {
		return nil, fmt.Errorf("-- Error reading config file: %s", err.Error())
	}
	err = yaml.Unmarshal(infoyml, yamlInfo)
	if err != nil {
		return nil, fmt.Errorf("-- Error unmarshalling config file: %s", err.Error())
	}
	return yamlInfo, nil
}

// parseRepoDatacite tries to access the request repository datacite file and
// parse the 'title' and the 'citation' from the files authors list.
// If the file cannot be accessed or there are any issues the script continues
// since both title and citation are not essential for the checklist.
func parseRepoDatacite(dcURL string) (string, string, error) {
	fmt.Printf("-- Loading datacite file at '%s'\n", dcURL)

	contents, err := readFileAtURL(dcURL)
	if err != nil {
		return "", "", err
	}

	yamlInfo := new(libgin.RepositoryYAML)
	err = yaml.Unmarshal(contents, yamlInfo)
	if err != nil {
		return "", "", fmt.Errorf("-- Error unmarshalling config file: %s", err.Error())
	}

	title := yamlInfo.Title
	authors := make([]string, len(yamlInfo.Authors))
	for idx, author := range yamlInfo.Authors {
		firstnames := strings.Fields(author.FirstName)

		var initials string
		for _, name := range firstnames {
			initials += string(name[0])
		}
		authors[idx] = fmt.Sprintf("%s %s", strings.TrimSpace(author.LastName), strings.TrimSpace(initials))
	}
	authlist := strings.Join(authors, ", ")
	return title, authlist, nil
}

// mkchecklistcli handles command line input options and ensures
// default values for missing entries.
func mkchecklistcli(cmd *cobra.Command, args []string) {
	// default configuration
	defaultcl := checklist{
		Regid:         "__ID__",
		Repoown:       "__OWN__",
		Repo:          "__REPO__",
		Regdate:       "__DATE__",
		Email:         "__MAIL__",
		Userfullname:  "__USER_FULL__",
		Title:         "__TITLE__",
		Citation:      "__CITATION__",
		Serveruser:    "__SERVER_USER__",
		Dirlocalstage: "__DIR_LOCAL_STAGE__",
		Ginserver:     "__GIN.SERVER__",
		Doiserver:     "__DOI.SERVER__",
		Dirdoiprep:    "__DIR_DOI_PREP__",
		Dirdoi:        "__DIR_DOI__",
	}

	// handling CLI config yaml; missing fields will keep the default values
	confile, err := cmd.Flags().GetString("config")
	if err != nil {
		fmt.Printf("-- Error parsing config flag: %s\n-- Exiting\n", err.Error())
		return
	}
	if confile != "" {
		loadedconf, err := readChecklistConfigYAML(&defaultcl, confile)
		if err != nil {
			fmt.Printf("%s\n-- Exiting\n", err.Error())
			return
		}
		defaultcl = *loadedconf

		// try to load title and citation from the gin datacite.yml
		baseURL := "https://gin.g-node.org"
		dcURL := fmt.Sprintf("%s/%s/%s/raw/master/datacite.yml", baseURL, defaultcl.Repoown, defaultcl.Repo)
		title, authors, err := parseRepoDatacite(dcURL)
		if err != nil {
			fmt.Printf("-- Error fetching repo datacite.yml: %s\n", err.Error())
		} else {
			if title != "" {
				defaultcl.Title = title
			}
			if authors != "" {
				defaultcl.Citation = authors
			}
		}
	}

	// handling CLI output file path; default is current directory
	var outpath string
	oval, err := cmd.Flags().GetString("out")
	if err != nil {
		fmt.Printf("Error parsing output directory flag: %s\n", err.Error())
	} else if oval != "" {
		outpath = oval
	}
	mkchecklist(defaultcl, outpath)
}
