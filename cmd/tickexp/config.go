package main

import (
	"fmt"
	"os"
	"strconv"
)

// default server port
const defaultPort = 8899

// default token expiration in minutes
const defaultExpiration = 1

// Configuration stores the basic server settings.
type Configuration struct {
	Port       uint16
	User       string
	Phrase     string
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

	port := uint16(defaultPort)
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

	cfg.User = readConf("tickuser")
	cfg.Phrase = readConf("tickphrase")
	if cfg.User == "" || cfg.Phrase == "" {
		return cfg, fmt.Errorf("missing user (%s) or phrase (%s)", cfg.User, cfg.Phrase)
	}

	exp := defaultExpiration
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
