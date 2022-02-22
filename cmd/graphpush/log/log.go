package log

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
)

var logfile *os.File
var logger *log.Logger
var logsize int

// trim reduces the size of a file to the provided filesize.
// It reads the contents and writes them back, removing the
// initial bytes to fit the limit. If any error occurs, it returns silently.
func trim(file *os.File, filesize int) {
	filestat, err := file.Stat()
	if err != nil {
		return
	}
	if filestat.Size() < int64(filesize) {
		return
	}
	contents := make([]byte, filestat.Size())
	nbytes, err := file.ReadAt(contents, 0)
	if err != nil {
		return
	}
	err = file.Truncate(0)
	if err != nil {
		fmt.Printf("error on file truncate: %q", err.Error())
		return
	}
	_, err = file.Write(contents[nbytes-filesize : nbytes])
	if err != nil {
		fmt.Printf("error writing file content: %q", err.Error())
	}
}

// Init initialises log file and logger.
func Init(logdir string, logname string, logfilesize int) error {
	logsize = logfilesize

	// Make sure the path to the logfile exists
	err := os.MkdirAll(logdir, os.ModePerm)
	if err != nil {
		return err
	}

	fp := filepath.Join(logdir, logname)
	logfile, err := os.OpenFile(fp, os.O_RDWR|os.O_APPEND|os.O_CREATE, 0644)
	if err != nil {
		return err
	}

	trim(logfile, logsize)

	logger = log.New(logfile, "", 0)
	Write("\n")

	logger.SetFlags(log.Ldate | log.Ltime)
	Write("=== LOGINIT ===")

	return nil
}

// Write writes a string to the log file if there is an initialized logger.
// Depending on the number of arguments, Write behaves like Print or Printf,
// the first argument must always be a string.
func Write(fmtstr string, args ...interface{}) {
	if logger == nil {
		return
	}
	logger.Printf(fmtstr, args...)
}

// ShowWrite writes a string to Stdout and passes
// the arguments on to the log Writer function.
func ShowWrite(fmtstr string, args ...interface{}) {
	fmt.Printf(fmtstr, args...)
	fmt.Println() // Append newline to stdout
	Write(fmtstr, args...)
}

// Close trims and closes the log file, errors are ignored.
func Close() {
	Write("=== LOGEND ===")
	trim(logfile, logsize)

	_ = logfile.Close()
}
