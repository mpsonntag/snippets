package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

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

func textPreFork(cl checklist) string {
	textblock := fmt.Sprintf(`
-[ ] manually fork repository to the 'doi' gin user
    - log on to gin.g-node.org using the "doi" user
    - fork https://gin.g-node.org/%s/%s
`, cl.Repoown, cl.Repo)

	return textblock
}

func textPreForkUpload(cl checklist, screenid string) string {
	dirpath := fmt.Sprintf("%s/10.12751/g-node.%s/%s", cl.Dirdoiprep, cl.Regid, strings.ToLower(cl.Repo))
	logfile := fmt.Sprintf("%s-%s.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo))

	textblock := fmt.Sprintf(`
-[ ] log on to the DOI server (%s) and move to %s
- Make sure all information has been properly downloaded to the staging directory and
  all annex files are unlocked and the content is present:
    -[ ] %s/annexcheck %s
    -[ ] find %s/10.12751/g-node.%s -type l -print
    -[ ] grep annex.objects $(find %s/10.12751/g-node.%s -type f -size -100c -print)
    -[ ] check that the content size of the repository and the created zip file matches
    -[ ] if there still are symlinks present or the content size does not match up, the zip
         file does not contain all required data. Run the next steps - the script will
         download all missing information and upload to the DOI fork. When recreating the
         zip file, all files will be manually unlocked first.
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S %s
    - sudo su root
    - ./doiforkupload %s > %s
-[ ] after detaching from the session, check the log file until the upload starts to avoid
     any security check issues.
     Also read the commit hash comparison line to check if the content of the repo has
     been changed after the DOI request has been submitted.
     tail -f %s
-[ ] if a) the logfile contains the line "repo was not at the DOI request state" the
     repository was changed after the DOI request and the uploaded archive content will
     most likely differ from the zip file content. If b) the 'tree' command showed symlinks or
     missing content, the zip file will also not contain the file content for all files.
       In this case use the 'makezip' bash script to recreate the zip file and
     copy it to the the DOI hosting folder.
-[ ] once the upload is done, check that the git tag has been created on the DOI fork repository at
     https://gin.g-node.org/doi/%s.`,
		cl.Doiserver, cl.Dirdoiprep, cl.Dirdoiprep, dirpath, cl.Dirdoiprep, cl.Regid,
		cl.Dirdoiprep, cl.Regid, screenid, dirpath, logfile, logfile, cl.Repo)

	return textblock
}

func textPreForkSync(cl checklist, screenid string) string {
	logfile := fmt.Sprintf("%s-%s.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo))

	textblock := fmt.Sprintf(`
-[ ] log on to the DOI server (%s) and move to %s
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s`, cl.Doiserver, cl.Dirdoiprep, screenid, cl.Repoown, cl.Repo, logfile)

	return textblock
}

func textPreGitTag(cl checklist) string {
	textblock := fmt.Sprintf(`
- create release tag on the DOI repository; run all commands using 'gin git ...'
  to avoid issues with local git annex or other logged git users.
    -[ ] cd %s/%s
    -[ ] check that "doi" is the set origin: sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin
`, cl.Dirdoiprep, strings.ToLower(cl.Repo), cl.Regid)

	return textblock
}

func textPreCleanup(cl checklist, screenid string, fulldoi bool) string {
	logfiles := fmt.Sprintf("%s-%s*.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo))

	dirpath := fmt.Sprintf("%s/10.12751/g-node.%s", cl.Dirdoiprep, cl.Regid)
	if fulldoi {
		dirpath = fmt.Sprintf("%s/%s", cl.Dirdoiprep, strings.ToLower(cl.Repo))
	}

	textblock := fmt.Sprintf(`
- cleanup directory once tagging is done
    -[ ] sudo rm %s -r
    -[ ] sudo mv %s/%s /home/%s/logs/
    -[ ] cleanup screen session: screen -XS %s quit`,
		dirpath, cl.Dirdoiprep, logfiles, cl.Serveruser, screenid)

	return textblock
}

// printPartPreDOI prints pre-registration block to file
func printPartPreDOI(cl checklist, fip *os.File) {
	textblock := fmt.Sprintf(`# Part 1 - pre registration

## Base request information
-[ ] check if the following information is correct; re-run script otherwise with updated config

    DOI request
    - Repository: %s/%s
    - User: (%s)
    - Email address: %s
    - DOI XML: %s:/data/doi/10.12751/g-node.%s/doi.xml
    - DOI target URL: https://doi.gin.g-node.org/10.12751/g-node.%s

    - Request Date (as in doi.xml): %s

`, cl.Repoown, cl.Repo, cl.Userfullname, cl.Email,
		cl.Doiserver, cl.Regid, cl.Regid, cl.Regdate)
	_, err := fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	_, err = fip.Write([]byte("## Base pre-registration checks"))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`
-[ ] GIN server (%s) check annex content
    - /gindata/annexcheck /gindata/gin-repositories/%s/%s.git`,
		cl.Ginserver, strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo))
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

- check the datacite content at
  https://gin.g-node.org/%s/%s
    -[ ] repo is eligible to be published via GIN DOI
    -[ ] the repo name is sufficiently unique to avoid clashes when
         forking to the DOI GIN user.
    -[ ] resourceType e.g. Dataset fits the repository
    -[ ] title is useful and has no typos
    -[ ] automated issues are all addressed
`, cl.Repoown, cl.Repo)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}
}

// printPartPreDOISemi prints semi automatic DOI pre-registration block to file
func printPartPreDOISemi(cl checklist, fip *os.File) {
	textblock := `
## Semi-automated DOI or DOI update
- use this section if there are no technical or other issues with the DOI request
  and skip the 'Full DOI' section.
- also use this section if there were no issues and an update to an existing DOI has
  been requested. The 'doiforkupload' script does both initial upload and update.`
	_, err := fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

- on the DOI server (%s) check the DOI directory content
    -[ ] zip file created in %s/10.12751/g-node.%s
    -[ ] check zip file content
         unzip -vl %s/10.12751/g-node.%s/10.12751_g-node.%s.zip
    -[ ] note zip size

-[ ] remove %s/10.12751/g-node.%s/.htaccess

- access https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check landing page in general
    -[ ] check title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and compare size on server with size in 'doi.xml'`,
		cl.Doiserver, cl.Dirdoi, cl.Regid, cl.Dirdoi, cl.Regid, cl.Regid, cl.Dirdoi, cl.Regid, cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = textPreFork(cl)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	randomID := randAlnum(5)
	screenid := fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randomID)
	textblock = textPreForkUpload(cl, screenid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = textPreCleanup(cl, screenid, false)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] Check link to archive repo on the DOI landing page works:
     https://doi.gin.g-node.org/10.12751/g-node.%s

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: %s/%s (10.12751/g-node.%s)

     This repository is prepared for the DOI registration.
`, cl.Regid, strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo), cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}
}

// printPartPreDOIFull prints optional full DOI pre-registration block to file.
func printPartPreDOIFull(cl checklist, fip *os.File) {
	textblock := `
## Full DOI
- This usually has to be done when
  a) the semi-automated process has failed or
  b) the user requested changes but needs to keep the originally issued DOI`
	_, err := fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = textPreFork(cl)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	randomid := randAlnum(5)
	screenid := fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randomid)
	textblock = textPreForkSync(cl, screenid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	ziplog := fmt.Sprintf("%s-%s_zip.log", strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo))
	filename := fmt.Sprintf("10.12751_g-node.%s.zip", cl.Regid)
	zipfile := fmt.Sprintf("%s/10.12751/g-node.%s/%s", cl.Dirdoi, cl.Regid, filename)

	textblock = fmt.Sprintf(`

-[ ] create DOI zip file
    - screen -r %s
    - sudo ./makezip %s > %s

-[ ] make sure there is no zip file in the target directory left
     from the previous registration process.

-[ ] sudo mv %s.zip %s`,
		screenid, strings.ToLower(cl.Repo), ziplog, strings.ToLower(cl.Repo), zipfile)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = textPreGitTag(cl)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = textPreCleanup(cl, screenid, true)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] edit %s/10.12751/g-node.%s/doi.xml file to reflect
     any changes in the repo datacite.yml file.
    - include the actual size of the zip file
    - check proper title and proper license
    - any added or updated funding or reference information
    - any changes to the 'resourceType'`, cl.Dirdoi, cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

- remove the .htaccess file
- create the DOI landing page in the local staging directory and move it to the DOI server
    -[ ] cd %s
    -[ ] gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml
    -[ ] scp %s/10.12751/g-node.%s/index.html %s@%s:/home/%s/staging
    - move to the DOI server staging directory
    -[ ] sudo chown root:root index.html
    -[ ] sudo mv index.html %s/10.12751/g-node.%s/index.html`,
		cl.Dirlocalstage, cl.Regid, cl.Dirlocalstage, cl.Regid, cl.Serveruser, cl.Doiserver,
		cl.Serveruser, cl.Dirdoi, cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

- https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check page access, size, title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and suggested size`, cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: %s/%s (10.12751/g-node.%s)

     This repository is prepared for the DOI registration.
`, strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo), cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}
}

// printPartPostDOI prints post-registration block to file.
func printPartPostDOI(cl checklist, fip *os.File) {
	fromdir := fmt.Sprintf("%s/keywords", cl.Dirlocalstage)
	toserver := fmt.Sprintf("%s@%s:/home/%s/staging", cl.Serveruser, cl.Doiserver, cl.Serveruser)

	textblock := fmt.Sprintf(`
# Part 2 - post registration
- re-create and deploy keywords if required
  -[ ] make sure github.com/G-Node/gin-doi is locally built and the 'gindoid' executable available
  -[ ] gin get G-Node/DOImetadata to local staging directory
  -[ ] create empty "keywords" directory and run the following from it
  -[ ] %s/gindoid make-keyword-pages %s/DOImetadata/*.xml
  -[ ] scp -r %s %s`, cl.Dirlocalstage, cl.Dirlocalstage, fromdir, toserver)

	_, err := fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`
  -[ ] connect to DOI server (%s)
  -[ ] sudo chown -R root:root /home/%s/staging/keywords
  -[ ] sudo mv %s/keywords %s/keywords_
  -[ ] sudo mv /home/%s/staging/keywords/ %s
  -[ ] check landing page and keywords online: https://doi.gin.g-node.org
  -[ ] sudo rm %s/keywords_ -r`, cl.Doiserver, cl.Serveruser,
		cl.Dirdoi, cl.Dirdoi, cl.Serveruser, cl.Dirdoi, cl.Dirdoi)

	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] connect to DOI server (%s) and update '%s/index.html';
     make sure there are no unintentional line breaks!
                        <tr>
                            <td><a href="https://doi.org/10.12751/g-node.%s">%s</a>
                            <br>%s</td>
                            <td>%s</td>
                            <td><a href="https://doi.org/10.12751/g-node.%s" class ="ui grey label">10.12751/g-node.%s</a></td>
                        </tr>

-[ ] update '%s/urls.txt': https://doi.gin.g-node.org/10.12751/g-node.%s`,
		cl.Doiserver, cl.Dirdoi, cl.Regid, cl.Title, cl.Citation, cl.Regdate,
		cl.Regid, cl.Regid, cl.Dirdoi, cl.Regid)

	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] git commit all changes in %s
    - sudo git add 10.12751/g-node.%s/
    - sudo git commit -m "New dataset: 10.12751/g-node.%s"

-[ ] commit keyword and index page changes
    - sudo git add keywords/
    - sudo git add index.html
    - sudo git add urls.txt
    - sudo git commit -m "Update index and keyword pages"

-[ ] set zip to immutable
    sudo chattr +i %s/10.12751/g-node.%s/10.12751_g-node.%s.zip

-[ ] cleanup any leftover directories from previous versions
     of this dataset in the %s/10.12751/ and
    %s/10.12751/ directories.

-[ ] email to user (check below)`, cl.Dirdoi, cl.Regid, cl.Regid, cl.Dirdoi, cl.Regid,
		cl.Regid, cl.Dirdoi, cl.Dirdoiprep)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}

	textblock = fmt.Sprintf(`

-[ ] close all related issues on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: %s/%s (10.12751/g-node.%s)

    Publication finished and user informed.
`, strings.ToLower(cl.Repoown), strings.ToLower(cl.Repo), cl.Regid)
	_, err = fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}
}

// printPartReadyEmail prints DOI registration ready email block to file.
func printPartReadyEmail(cl checklist, fip *os.File) {
	// a bit nasty but I think good enough
	citeyear := time.Now().Format("2006")

	textblock := fmt.Sprintf(`
# Part 3 - eMail to user
-[ ] make sure the publication reference text does apply, remove otherwise

%s

CC: gin@g-node.org

Subject: DOI registration complete - %s/%s

Dear %s,

Your dataset with title
  %s

has been successfully registered.

The DOI for the dataset is
  https://doi.org/10.12751/g-node.%s

Please always reference the dataset by its DOI (not the link to the
repository) and cite the dataset as
  %s (%s)
  %s
  G-Node. https://doi.org/10.12751/g-node.%s

If this is data supplementing a publication and if you haven't done so already, we kindly request that you:
- include the new DOI of this dataset in the publication as a reference, and
- update the datacite file of the registered dataset to reference the publication, including its DOI, once it is known.

The latter will result in a link in the Datacite database to your publication and will increase its discoverability.

Best regards,

  German Neuroinformatics Node
`, cl.Email, cl.Repoown, cl.Repo, cl.Userfullname, cl.Title, cl.Regid, cl.Citation,
		citeyear, cl.Title, cl.Regid)
	_, err := fip.Write([]byte(textblock))
	if err != nil {
		fmt.Printf("Error writing to checklist file: %s", err.Error())
		return
	}
}

func writeChecklistFile(cl checklist, fip *os.File) {
	printPartPreDOI(cl, fip)
	printPartPreDOISemi(cl, fip)
	printPartPreDOIFull(cl, fip)
	printPartPostDOI(cl, fip)
	printPartReadyEmail(cl, fip)
}

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

func handleChecklistContent(cl checklist, outpath string) {
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

	// prepare template data
	fullcl := ChecklistTemplate{
		CL:               cl,
		RepoLower:        strings.ToLower(cl.Repo),
		RepoownLower:     strings.ToLower(cl.Repoown),
		SemiDOIScreenID:  fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randAlnum(5)),
		FullDOIScreenID:  fmt.Sprintf("%s-%s", strings.ToLower(cl.Repoown), randAlnum(5)),
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

// mkchecklist prepares the output file and calls the function
// handling the file content.
func mkchecklist(cl checklist, outpath string) {
	handleChecklistContent(cl, outpath)
}

// readConfigYAML parses the config info and returns a filled checklist struct.
func readConfigYAML(yamlInfo *checklist, confile string) (*checklist, error) {
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
	loadedconf, err := readConfigYAML(&defaultcl, confile)
	if err != nil {
		fmt.Printf("%s\n-- Exiting\n", err.Error())
		return
	}
	defaultcl = *loadedconf

	// handling CLI output file path; default is current directory
	var outpath string
	oval, err := cmd.Flags().GetString("out")
	if err != nil {
		fmt.Printf("Error parsing output directory flag: %s\n", err.Error())
	} else {
		outpath = oval
	}
	mkchecklist(defaultcl, outpath)
}
