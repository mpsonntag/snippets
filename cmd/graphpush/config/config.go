package config

import (
	"os"
	"path/filepath"
)

// Directories used by the server for temporary and long term storage.
type Directories struct {
	Source string `json:"source"`
	Log    string `json:"log"`
}

// Denotations provide any freuquently used file names or other denotations
// e.g. validation result files, badge or result folder names.
type Denotations struct {
	LogFile string `json:"logfile"`
}

// Settings provide the default server settings.
// "Validators" currently only supports "BIDS".
type Settings struct {
	Port     string `json:"port"`
	LogSize  int    `json:"logsize"`
	MetaUser string `json:"metauser"`
	MetaPW   string `json:"metapw"`
}

// ServerCfg holds the config used to setup the gin validation server and
// the paths to all required executables, temporary and permanent folders.
type ServerCfg struct {
	Settings Settings    `json:"settings"`
	Dir      Directories `json:"directories"`
	Label    Denotations `json:"denotations"`
}

var defaultServer = ServerCfg{
	Settings{
		Port:    "6066",
		LogSize: 1048576,
	},
	Directories{
		Source: filepath.Join(os.Getenv("GRAPHPUSHSOURCE")),
		Log:    filepath.Join(os.Getenv("GRAPHPUSHHOME")),
	},
	Denotations{
		LogFile: "graphpush.log",
	},
}

// Read returns the default server configuration.
func Read() ServerCfg {
	return defaultServer
}

// Set sets the server configuration.
func Set(cfg ServerCfg) {
	defaultServer = cfg
}
