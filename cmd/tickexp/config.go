package main

import (
	"fmt"
	"os"
	"strconv"
)

type Configuration struct {
	Port uint16
	User string
	Phrase string
	Expiration int
}

// ReadConf returns the value of a configuration env variable.
// If the variable is not set, an empty string is returned (ignores any errors).
func readConf(key string) string {
	value, _ := os.LookupEnv(key)
	return value
}

func loadconfig() (Configuration, error) {
	cfg := Configuration{}

	port := uint16(8899)
	portstr := readConf("port")
	if portstr != "" {
		portint, err := strconv.ParseUint(portstr, 10, 16)
		if err != nil {
			fmt.Printf("Could not parse port %q, using default %d", portstr, port)
		} else {
			port = uint16(portint)
		}
	}
	cfg.Port = port

	cfg.User = readConf("user")
	cfg.Phrase = readConf("phrase")
	if cfg.User == "" || cfg.Phrase == "" {
		return cfg, fmt.Errorf("missing user (%s) or phrase (%s)", cfg.User, cfg.Phrase)
	}

	exp := 1
	expstr := readConf("expiration")
	if expstr != "" {
		expint, err := strconv.Atoi(expstr)
		if err != nil {
			fmt.Printf("Could not parse expiration %q, using default %d", expstr, expint)
		} else {
			exp = expint
		}
	}
	cfg.Expiration = exp

	return cfg, nil
}
