package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/url"
	"os"
	"strings"
)

func intSeq() func() int {
	i := 0
	return func() int {
		i += 1
		return i
	}
}

func main() {
	nextInt := intSeq()
	fmt.Println(nextInt())
	fmt.Println(nextInt())
	newInts := intSeq()
	fmt.Println(newInts())
	fmt.Println(nextInt())

	s := "abcä⌘"
	b := []byte(s)
	fmt.Printf("len(s): %d, len(b): %d\n", len(s), len(b))
	for i, v := range b {
		fmt.Printf("(%d)%s/", i, string(v))
	}
	fmt.Println("")
	for i, v := range s {
		fmt.Printf("(%d)%s/", i, string(v))
	}
	fmt.Println("")

	x := false
	var y []byte

	if x && y[0] != 'c' {
		fmt.Println("I should fail hard!")
	} else {
		fmt.Println("I stopped because the first condition was wrong!")
	}

	fmt.Println("-------------------------------")
	q := &url.Values{}
	q.Add("vals", "ä : + / ü ö ß and some normal values as well")
	s = q.Encode()
	fmt.Printf("Encoded Query: %s\n", s)
	val, _ := url.ParseQuery(s)
	fmt.Printf("Decoded Query: %s\n", val.Get("vals"))

	fmt.Println("\n----- try opening non existing file ---")
	const fn = "IdoNotExist"
	f, err := ioutil.ReadFile(fn)
	if err != nil {
		fmt.Printf("Cannot open file %q\n", fn)
	} else {
		fmt.Printf("I shall print this thing: %q\n", string(f))
	}

	fmt.Println("------ test struct field pointer -------------------------")
	type blub struct {
		s *string
		b *bool
		i *int
	}

	var test blub

	fmt.Printf("Initialized:")
	fmt.Printf("Instance: %v, s: %v, b: %b, i: %v\n", test, test.s, test.b, test.i)

	b = []byte(`{"s":"somestring"}`)
	json.Unmarshal(b, &test)
	fmt.Printf("Instance: %v, s: %v, b: %b, i: %v\n", test, test.s, test.b, test.i)

	fmt.Println("\n------ test escape missing JSON fields -------------------------")

	fmt.Println("")
	b = []byte(`{}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"somefield":"somevalue"}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":"somevalue"}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":true}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":false}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":null}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":True}`)
	testMissingJSONFields(b)

	fmt.Println("")
	b = []byte(`{"public":"true"}`)
	testMissingJSONFields(b)

	fmt.Println("\n------ test write non existing and existing file -------------------------")
	testWriteFile("this is my content for a non existing file", "writeTest.txt")
	testWriteFile("this is my content for a non existing file", "writeTestOR.txt")
	testWriteFile("this is my content for an already existing file", "writeTestOR.txt")

	fmt.Println("\n------ map test -------------------------")
	superMapToTheRescue := make(map[string]string)
	superMapToTheRescue["a"] = "a value"
	superMapToTheRescue["b"] = "b value"

	for k, v := range superMapToTheRescue {
		fmt.Printf("Key: %q, Value: %q\n", k, v)
	}

	fmt.Println("\n------ delete test -------------------------")
	filename := "tmpfile.tmp"
	err = ioutil.WriteFile(filename, []byte("hurra"), 0666)
	if err != nil {
		fmt.Printf("Error creating file: %v\n", err)
	} else {
		fmt.Println("Remove existing file.")
		err = os.Remove(filename)
		if err != nil {
			fmt.Printf("%v\n", err)
		} else {
			fmt.Println("Remove non existing file.")
			err = os.Remove(filename)
			if err != nil && err == os.ErrNotExist {
				fmt.Printf("File does not exist: ", err)
			} else if err != nil {
				fmt.Printf("%v\n", err)
			} else {
				fmt.Println("All removed.")
			}
		}
	}

	fmt.Println("\n--------------- init boolean test ----------------")

	type mrgs struct {
		Contained    bool
		NotContained bool
	}

	useMe := mrgs{}

	fmt.Printf("This is contained: \t%v\n", useMe)

	decodeThis := `{ "contained": true, "notContained": true }`

	decoder := json.NewDecoder(strings.NewReader(decodeThis))
	err = decoder.Decode(&useMe)
	if err != nil {
		fmt.Printf("Error decoding: %v\n", err)
	}
	fmt.Printf("This is now contained: \t%v\n", useMe)
}

func testMissingJSONFields(b []byte) {
	var setPublic bool
	var vis interface{}

	err := json.Unmarshal(b, &vis)
	if err != nil {
		fmt.Printf("Error unmarshalling interface (%v): %v\n", vis, err)
		return
	}
	m := vis.(map[string]interface{})
	if val, ok := m["public"]; ok {
		switch val.(type) {
		case bool:
			setPublic = val.(bool)
		default:
			fmt.Println("input did not contain required field type")
			return
		}
	} else {
		fmt.Println("input did not contain required field")
		return
	}

	fmt.Printf("All is well, field had value: %t\n", setPublic)
}

func testWriteFile(content, filename string) error {
	return ioutil.WriteFile(filename, []byte(content), 0666)
}

func testFileExclusionWrapper() {
	test := []string{"ab", "cd", "ef"}
	testFileExclusion(test, "one", "two", "three", "ab")
}

func testFileExclusion(exclude []string, source ...string) {
	for _, src := range source {
		var skip bool
		for i := range exclude {
			if exclude[i] == src {
				skip = true
				break
			}
		}
		if !skip {
			fmt.Println(src)
		} else {
			fmt.Printf("Excluding '%s'\n", src)
		}
	}
}
