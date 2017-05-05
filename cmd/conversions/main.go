package main

import (
	"fmt"
	"reflect"
	"strconv"
)

type gitCS struct {
	Commit  string
	Subject string
}

type wireCS struct {
	Commit  string `json:"commit"`
	Subject string `json:"subject"`
}

func main() {
	g := make([]gitCS, 10)
	for i := 0; i < 10; i++ {
		fmt.Printf("Currval: %q\n", strconv.Itoa(i))
		g[i].Commit = strconv.Itoa(i)
		g[i].Subject = strconv.Itoa(i)
	}

	w := make([]wireCS, len(g))

	for i, v := range g {
		// go version 1.8 specific, will panic with any other version
		// w[i] = wireCS(v)

		// version unspecific
		w[i].Commit = v.Commit
		w[i].Subject = v.Subject +"-"
	}
	fmt.Printf("gitCS:  %v, Type: %q, Type content: %q\n", g, reflect.TypeOf(g), reflect.TypeOf(g[0]))
	fmt.Printf("wireCS: %v, Type: %q, Type content: %q\n", w, reflect.TypeOf(w), reflect.TypeOf(w[0]))
}
