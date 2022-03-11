package main

import (
	"os"
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
