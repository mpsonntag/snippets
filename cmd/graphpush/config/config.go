package config

import (
	"os"
	"path/filepath"
)

// Directories used by the server for temporary and long term storage.
type Directories struct {
	Temp   string `json:"temp"`
	Source string `json:"source"`
	Log    string `json:"log"`
}

// Settings provide the default server settings.
type Settings struct {
	Port     string `json:"port"`
	LogSize  int    `json:"logsize"`
	LogFile  string `json:"logfile"`
	MetaUser string `json:"metauser"`
	MetaPW   string `json:"metapw"`
}

// ServerCfg holds the config used to setup the gin validation server and
// the paths to all required executables, temporary and permanent folders.
type ServerCfg struct {
	Settings Settings    `json:"settings"`
	Dir      Directories `json:"directories"`
}

var defaultServer = ServerCfg{
	Settings{
		Port:    "6066",
		LogSize: 1048576,
		LogFile: "graphpush.log",
	},
	Directories{
		Source: filepath.Join(os.Getenv("GRAPHPUSHSOURCE")),
		Log:    filepath.Join(os.Getenv("GRAPHPUSHHOME")),
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
