# Go

# Packages:
- Go programs are organized in packages.
- Programs require a package `main`.
- Further packages can be used via `import`
- Imports can be written as:

        import "fmt"
        import "math"

    or as

        import (
            "fmt"
            "math"
        )

- Aliases to imports can be assigned

        // contents of the imported package can be used via "short"
        import short "totallyUnGoLikelongAndWindingPackageName"

- Unused imports are not allowed.
- NOTE - Jumping ahead: Every package can contain an `init()` function, which is executed once upon import. If only
code within the `init()` function of a package is required, but nothing of the package itself, it would be an
unused import. To still allow this import, the following code can be used. `_` is always used to immediately 
discard any data that is being assigned to it.

        _ import "fmt"

- To see in which order packages are imported and in which order the respective `init()` functions 
are executed see section "Go initialization" below.


# Functions:
- Go is a statically typed language (type is known at compile time).
- Functions take zero or more arguments, argument and return types have to be provided.
- The types of function arguments are defined AFTER the name of the argument.

        func add(x int, y int) int {
            return y + x
        }

- Functions can return multiple values.
- Return values of functions can be ignored using `_`.

        func swap(fst string, snd string) (string, string) {
            return snd, fst
        }

        func main() {
            a, b := swap("I am", "First")
            fmt.Println(a, b, "says Mr Yoda")

            c, _ := swap("Ignored", "I shall be")
            fmt.Println(c, "a king")
        }

- Go is a first order language: Functions can be passed to other functions as arguments and values.

        func compute(fn func(float64, float64) float64) float64 {
            return fn(3, 4)
        }

        func main() {
            hypot := func(x, y float64) float64 {
                return math.Sqrt(x*x + y*y)
            }
            fmt.Println("hypot", hypot(5, 12))
    
            fmt.Println("compute(hypot)", compute(hypot))   // passes hypot without arguments to compute. 
                                                            // Compute uses hypot with its own values 3, 4 and
                                                            // returns the return value of hypot.
            fmt.Println("compute(math.Pow)", compute(math.Pow))
        }


### Closures
- are anonymous functions
- are returned by a function
- have access to the variables that have been defined by the surrounding function - but once the closure is returned,
there is no possible ways to access these variables except when the closure is executed (closure ... closed function?)
- keep track of the state of their contained variables and will work with them each time the variable 
that the anonymous function has been assigned to is accessed.

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
        }


# Variables
- Variables are declared via the keyword `var` and require a type after the variable name.
- Variables can be declared at both package and function level. Variables can also be initialized when they are declared.

        var a bool
        var d int = 10
        func main() {
            var i int
            fmt.Println("I spy with my little i", i, "which is", a, "ok and also very", d, "dent")
        }

- NOTE: Depending on the type, the variables are initialized with initial values matching the type 
(e.g. bool: false, byte, int, float, etc: 0, string: "") - and not with null/nil.
- NOTE: If a variable is declared at package level, it will be initialized even BEFORE the `init()` function 
of the package.
- Inside a function the variable declaration can be shortened by using the short assignment `:=` with implicit type,
meaning, that the type will be inferred from whatever comes after this short assignment.

        fancyPants := "The fairy queen short assigns fancy pants which are made of"
        fmt.Println(fancyPants, reflect.TypeOf(fancyPants))
        fancyPants = "The fairy queen short assigns fancy pants which are made of reassigned"
        fmt.Println(fancyPants, reflect.TypeOf(fancyPants))


# Constants
- Constants are declared like variables using the keyword `const`.
- Constants can only be initialized at the same time as their declaration, but can take advantage of type inference.

        const epicPants string = "Her epic pants on the other hand are very constant"
        fmt.Println(epicPants)
        const epicShirt = "As is her epic shirt, which interestingly is also made of inferred"
        fmt.Println(epicShirt, reflect.TypeOf(epicShirt))

        const intern = 10
        const lowFloat = 1.2
        fmt.Println("Meanwhile the", reflect.TypeOf(intern), "does not even know its inferred", 
                        reflect.TypeOf(lowFloat), "value")


# Basic types
- The available basic types are

        bool
        string
        int  int8  int16  int32  int64
        uint uint8 uint16 uint32 uint64 uintptr
        byte // alias for uint8
        rune // alias for int32; represents a Unicode code point
        float32 float64
        complex64 complex128

- NOTE! `int, uint, uintptr` types are 32bit/64bit on 32/64bit systems respectively.
- More information about strings, bytes and runes can be found [in this blog entry](https://blog.golang.org/strings).
- Crashcourse about the difference of int and uint and how they can be represented in memory can be found [here](http://stackoverflow.com/a/13422442).

### String, runes, UTF-8 code points
- In Go a string is a read-only slice of bytes (of any format e.g. Unicode, UTF-8, etc).
- Since a string is a slice of bytes, the individual bytes of a string can be accessed by index.
        e.g. `sampleString[0]` yields the byte of string `sampleString` at index 0.

- go source code is always UTF-8
- it is assumed, that strings contain proper UTF-8 code points - but that does not necessarily have to be true;
this depends from where the string came from.
- a rune can hold a proper UTF-8 code point
- if we `for range` over a `[]byte`, the individual pieces will be of type `byte`=`uint8`
- if we `for range` over a `string`, the individual pieces will be of type `rune`=`int32`=UTF-8 code points

The go library unicode/utf8 provides support for validating and working with UTF8 strings, 
find it [here](http://golang.org/pkg/unicode/utf8/).
Find out more about unicode characters [here](http://unicode.org/).

- it seems to work like this (with utf-8 for sure):
    - if we have a string, this is actually a slice of bytes.
    - we walk through every byte.
    - we check the first bit of the first byte.
    - if the first bit of the first byte is a 0, we are dealing with an ASCII character, which is 
        exactly one byte long. We can look up in the ASCII table, which character it is, do whatever we
        want with it and move on to interpreting the next byte!
    - if the first bit of the first byte was a 1, then the byte encodes for a code point that requires more than
        just one byte of length and it has to be further looked up, which character it is.
- look at the output from the following experiment to make it clearer:

        s := "abcä⌘"
        b := []byte(s)
        for i, v := range b {
            fmt.Printf("(%d)%s / ", i, string(v))
        }
        // (0)a / (1)b / (2)c / (3)Ã / (4)¤ / (5)â / (6) / (7) /
        for i, v := range s {
            fmt.Printf("(%d)%s/", i, string(v))
        }
        // (0)a / (1)b / (2)c / (3)ä / (5)⌘ /

For more information check the description and example part [on wikipedia](https://en.wikipedia.org/wiki/UTF-8#Description)  
and read the [minimal unicode](http://www.joelonsoftware.com/articles/Unicode.html) blogpost from Joel Spolsky.

# Type conversion
- The expression `T(v)` converts value `v` to type `T`.
- NOTE: Go requires explicit conversion between different types.

        hui := 49
        pfui := math.Sqrt(float64(hui))
        var wui int = int(pfui)
        fmt.Println(wui)


# Control structures

### For
- Go has only one loop structure, the `for` loop
- The syntax is `for [init statement]; [terminator condition]; [post current iteration statement] {}`

        for i := 0; i < 4; i++ {
            fmt.Println("The fairy queen does situp number", i)
        }
        fmt.Println("And now she's having a break.")

- The first and the last statement of a `for` loop is optional:

        moreSitups := 4
        for moreSitups < 10 {
            fmt.Println("The fairy queen does situp number", moreSitups)
            moreSitups = moreSitups + 1
        }
        fmt.Println("And now she's tired and eats icecream.")


### If
- The plain `if` looks like this:

        evenMoreSitups := 10
        if evenMoreSitups > 9 {
            fmt.Println("No, thank you!")
        }

- There is a "short" statement that can be executed immediately before an `if` condition.

        func pow(x, n, lim float64) float64 {
            if v := math.Pow(x, n); v < lim {
                return v
            }
            return lim
        }
    
        func main() {
            fmt.Println(
                pow(3, 2, 10),
                pow(3, 3, 20),
            )
        }

- `if - else if - else` is nothing fancy and looks like this:

        if [condition] {
        } else if [condition] {
        } else {
        }


### Switch
- `switch` has `case` and `default` and it supports initial statements. `switch` breaks once a case has matched; 
`default` will only be reached, if no case has matched

        switch os := runtime.GOOS; os {
        case "darwin":
            fmt.Println("OS X.")
        case "linux":
            fmt.Println("Linux.")
        default:
            // freebsd, openbsd,
            // plan9, windows...
            fmt.Printf("%s.", os)
        }

- `switch` supports fallthrough behavior; if a case contains `fallthrough`, it will fall into the next
case, without checking.

        func test(value int) {
            switch value {
            case 3:
                fmt.Println("3")
            case 2:
                fmt.Println("2")
                fallthrough
            case 1:
                fmt.Println("1")
                fallthrough
            case 0:
                fmt.Println("0")
                break
            }
        }

- `switch` without a condition is used instead of if-else chains:

        switch {
        case t.Hour() < 12:
            fmt.Println("Good morning!")
        case t.Hour() < 17:
            fmt.Println("Good afternoon.")
        default:
            fmt.Println("Good evening.")
        }


### Defer
- The `defer` statement defers the execution of a function until the surrounding function ends.
- The defer's arguments are evaluated immediately, but the function call is not executed until 
the end of the surrounding function.

        xx := "a Yoda"
        yy := "the fairy queen is not"
        defer fmt.Println(xx)
        xx = "something else"
        fmt.Println(yy)

- Defers are pushed onto a stack, which means: last in first out...
- If a `panic` occurs
    - the surrounding function will stop
    - all deferred functions of the stopped function to this point will be executed
    - the `panic` is then returned to the caller of the surrounding function and run up the stack until all functions
    of the current go routine have ended.
    - then the program crashes.

- find more information [here](https://blog.golang.org/defer-panic-and-recover)

# Pointers
- A pointer holds the memory address of a variable.
- Pointers are initialized with value nil.
- Go has no pointer arithmetic
(find out more about pointer arithmetic [here](https://www.cs.umd.edu/class/sum2003/cmsc311/Notes/BitOp/pointer.html)).
- `*T` is of type pointer to a value of type `T`, e.g. `var p *int`
- The `&` operator generates a pointer to its corresponding variable (it returns the memory address of the variable):

        var p *int
        i := 42
        p = &i // &i returns *int in this case

    or

        b := &i

- The `*` operator enables access to the value of the variable a pointer is associated with.

        fmt.Println(*p) // read value of i through pointer p
        *p = 21         // set value of i through pointer p

- The following example shows basic pointer usage and unusage:

        func testPointer() {
            var i int = 21
            var x *int
    
            //fmt.Println("*x has value:\t", *x) // Since the pointer points nowhere at the moment, this leads to panic.
            //x = 12 // Since this is a pointer, it can only hold addresses, no actual value and this leads to panic.
    
            fmt.Println("x has value:\t", x)        // <nil>
    
            x = &i
            fmt.Println("x has value:\t", x)        // [memory address of 'i']
            fmt.Println("&x has value:\t", &x)      // [memory address of 'x']
            fmt.Println("*x points to:\t", *x)      // 21
            fmt.Println("i before:\t", i)           // 21
    
            *x = 22
            fmt.Println("i after:\t", i)            // 22
            fmt.Println("x has value:\t", x)        // [memory address of 'i']
    
            *x = *x/2
            fmt.Println("i has been divided:\t", i) // 11
        }

NOTE: pointers are usually used with `structs` (see below), larger constructs that might have large
      memory requirements. Instead of passing the structs from function to function, it
      is probably more efficient to just pass the memory address to the struct and 
      fetch the content only where it is actually required.


### `new`
- the `new` function can be used to get a pointer to a new value
- it allocates enough memory to fit the value, the value will be the zero value corresponding to the used value type.
- it returns a pointer to that allocated memory

        type customType struct{
            customField string
        }

        x := new(customType) // returns *customType
        y := &customType     // returns *customType

### When to use
Find out when to use pointers to basic types 
[here](https://dhdersch.github.io/golang/2016/01/23/golang-when-to-use-string-pointers.html). 

# Structs
- A `struct` is a collection of fields.
- The fields of a `struct` can be accessed using a dot. Struct fields can also be accessed via a struct pointer.
- The fields of a `struct` will be initialized with default values according to the field type, if they are not set at struct initialization.

        type Vertex struct {
            X int
            Y int
        }

        func useVertex() {
            var va Vertex = Vertex{1, 2}
            vb := Vertex{}
            fmt.Println("Struct access: va:", va, "vb:", vb)
            fmt.Println("Struct field access: va.X:", va.X, "vb.X:", vb.X)
    
            var pa *Vertex = &va
            pb := &vb
            pb.X = 120
            fmt.Println("Struct pointer access: va.X:", pa.X, "vb.X:", pb.X)
            *pb = *pa
            fmt.Println("Pointer replace of struct vb:", vb)
        }

- Note: Visibility of structs and their fields is defined by their first letter. If a struct or a field of a struct 
starts with a capital letter, it is public and can be accessed outside of the package. If it starts with a lower case 
letter, it is only accessible within the same package!

[xxx] I'm here!

# Arrays
- `[n]T` is an array of `n` values of type `T`.
- Arrays cannot be resized.

        var story [6]string
        story[0] = "\n"
        story[1] = "..."
        story[2] = "happily"
        story[3] = "ever"
        story[4] = "after"
        story[5] = "(but not really)"
        fmt.Println(story[0], "Tell me the story ...", story[0], story)


### Slices of an array
- Slices point to arrays.
- Slicing a slice will only change the pointer, but never the underlying array, 
even if the slice only points to a portion of the array. 
Until a slice points to a completely different array, the underlying array will always be kept in memory.
- `[]T` is a slice with elements of type `T`.

        primes := []int{2, 3, 5, 7, 11, 13}
        fmt.Println("primes ==", primes)

- Slices can be multi dimensional and can contain any type including other slices:

        import "fmt"
        import "strings"
    
        func printBoard {
            board := [][]string{
                []string{"_", "_", "_"},
                []string{"_", "_", "_"},
                []string{"_", "_", "_"},
            }
    
            for i := 0; i < len(board); i++ {
                fmt.Printf("%s\n", strings.Join(board[i], " "))
            }
        }

- Slices can be re-sliced using the syntax `s[lo:hi]` where `lo` and `hi` are integers corresponding to the slice index.
- `lo` is always included, `hi` is always excluded. `s[lo:lo]` is empty, `s[lo:lo+1]` contains exactly one element.
- A missing `lo` index implies an index of 0

        s := []int{1, 2, 3, 4, 5, 6}
        fmt.Println(s[:3])

- A missing `hi` index implies `len(s)`

        s := []int{1, 2, 3, 4, 5, 6}
        fmt.Println(s[3:])

- New slices are created using the `make` function. The two additional parameters are `length` and `capacity`. 
- A slice cannot grow longer than its capacity. If this happens, a new underlying array is created, doubling the capacity, 
copying the contents of the original array into the new one, replacing the pointer of the slice with a pointer to the 
new array and updating the capacity of the slice. 

        s := make([]int, 2, 5)
            // Creates an empty slice with an underlying array of length 2 and capacity 5. 
            // It will initialize only the first two entries of the underlying array with 0.

- Go provides a built-in append function for slices. Since slices are wrappers for arrays which only contain 
the pointer to an array and the len and capacity of the array the slice actually points to, an append will 
under the hood create a new array and reassign the pointer of the slice to the new array.

        s := make([]int, 1, 2)
        s = append(s, 1, 2) // results in [0 1 2], len=3, cap=4
                            // In this example the underlying array had been initilized with one default value = 0. 
                            // Two values were appended leading to [0 1 2]. 
                            // Since the original capacity was 2, append created a new array with doubled capacity, 
                            // copied the contents of the original array (0) to the new one, appended the two new values 
                            // and returned a pointer to the new array.


- NOTE: The zero value of a slice without a length is `nil`

        var s []int
        fmt.Println(s, len(s), cap(s))
        if s == nil {
            fmt.Println("nil!")
        }

- Slices can be used with range. When looping over a slice, 
`range` returns the current index and the value of the slice at that index for each iteration.

        var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}
    
        for i, v := range pow {
            fmt.Printf("2**%d = %d\n", i, v)
        }


# Maps
- A map maps keys to values.
- The syntax is `map[type of key]type of value`.
- New maps are created with `make`.

        m := make(map[string]int)
        m["one"] = 1
        m["two"] = 2
        m["three"] = 3
    
        fmt.Println(m, m["one"])

- Elements of a map can be entered, updated, deleted and checked for existence via the key.

        m := make(map[string]int)
        m["iDoNotExist"] // returns 0
        m["iExist"] = 1 // create
        m["iExist"] = 2 // update
        delete(m["iExist"]) // delete; 
        v, ok := m["iExist"] // check for existence, v contains the return value, ok true if the key exists, false otherwise


# Methods
- Go does not provide classes, but `methods` can be defined for custom `types`.
- Within a package, functions can be defined for "receivers" using syntax `func (valName receiverType) FuncName() returnType`
- Methods can be called on an instance of their receiver.
- In the following example, a method "FullName" is defined for a struct "Person". 

        // Define custom type Person
        type Person struct {
            fname, lname string
        }
    
        // Define method for custom type
        func (p Person) FullName() string {
            return p.fname +" "+ p.lname
        }
    
        func main() {
            p := Person{"Blub", "Blubberich"}
            fmt.Println(p.FullName())
        }

- The correct wording is "A method is a function with a receiver argument"
- NOTE: Methods work with copies of values. If the receiver value is manipulated within a method, 
this will NOT change the original value. If methods should manipulate the actual value, the receiver of a method 
has to be a pointer!

        type Person struct {
            fname, lname string
        }
    
        func (p Person) PrintFullName() string {
            p.fname = "Mr "+ p.fname
            return p.fname +" "+ p.lname
        }
    
        func (p *Person) UpdateFname() string {
            p.fname = "new"
            return p.fname +" "+ p.lname
        }
    
        func main() {
            p := Person{"Blub", "Blubberich"}
            fmt.Println(p.PrintFullName(), p.fname) // p.fname has not changed
            fmt.Println(p.UpdateFname(), p.fname) // p.fname has been updated
        }

- NOTE: methods take both values ("p" in our example) as well as pointers ("&p") as receivers. 
Go conveniently interprets "p" as "&p" in our example since the UpdateFname method has a pointer receiver.


# Interfaces
- An interface is a specific `type`, that is defined by / represents a set of method signatures.
- Go interfaces are implemented implicitly. There is no statement, that a type is implementing an interface using 
e.g. an "implements" keyword. Only if a type actually implements all interface methods, it implements the interface. 
- Example of an interface: *Stringers*; One of the most ubiquitous interfaces is Stringer, defined by the fmt package. 
Before printing a value, fmt will check, if the value has implemented the `Stringer` interface
and use the corresponding methods return value to print.

        type Stringer interface {
            String() string
        }

- A Stringer is a type that can describe itself as a string. The fmt package (and many others) 
look for this interface to print values. An implementation of this interface would be: 

        type Person struct {
            Name string
            Age  int
        }
    
        func (p Person) String() string {
            return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
        }
    
        func main() {
            a := Person{"Arthur Dent", 42}
            z := Person{"Zaphod Beeblebrox", 9001}
            fmt.Println(a)          // prints "Arthur Dent (42 years)"
            fmt.Println(z)          // prints "Zaphod Beeblebrox (9001 years)"
        }

- A variable of interface type stores a pair: the actual value and the type of that value.


## The empty interface
- `interface{}` can hold any value; the empty interface can hold zero or more methods.
- This can be used in reflection, when we want to assign something "dynamic" at a certain point in our code.
 
        var r io.Reader
        tty, err := os.OpenFile("/dev/tty", os.O_RDWR, 0)
        if err != nil {
            return nil, err
        }
        r = tty                 // contains (tty, *os.File) ... value und type of value
 
        var w io.Writer
        w = r.(io.Writer)       // type assertion ... its asserted, that the type of r actually 
                                // implements the io.Writer interface. This might fail, if r does not implement
                                // all the io.Writer methods
        
        var empty interface{}
        empty = w               // Since an empty interface can hold ANY value this works nicely and accepts any methods.
                                // The value pair contained in this interface will always be (value, concrete type)

- Find more detailed information about interfaces in [this blog post by Russ Cox](http://research.swtch.com/interfaces).
- TO CHECK: Not sure how interfaces work over different packages, and when which code is executed.
- Using reflection, it can be tested, if sthg passed in via an empty interface actually provides the required method:

        type Stringer interface {
            String() string
        }
        
        func ToString(any interface{}) string {
            if v, ok := any.(Stringer); ok {
                return v.String()
            }
            switch v := any.(type) {
            case int:
                return strconv.Itoa(v)
            case float:
                return strconv.Ftoa(v, 'g', -1)
            }
            return "???"
        }


# Reflection
- Now that we know how interfaces work, we can have a look at reflections in Go!
- Check [this blog post about reflections](http://blog.golang.org/laws-of-reflection) for more details.
- [TODO] - read above.


# Errors
- The `error` type is a built-in interface; when printing values, the fmt package will 
look for an implementation of `error` before printing a value.

        type error interface {
            Error() string
        }

- An example of an error implementation:

        type MyError struct {
            When time.Time
            What string
        }
    
        func (e *MyError) Error() string {
            return fmt.Sprintf("at %v, %s",
                e.When, e.What)
        }
    
        func run() error {
            return &MyError{
                time.Now(),
                "it didn't work",
            }
        }
    
        func main() {
            if err := run(); err != nil {
                fmt.Println(err)
            }
        }


# Visibility
- Constants, variables, structs and functions that have an identifier starting with an upper case letter 
can be accessed from outside of the package.
- The same with an identifier starting with a lower case letter can only be accessed within the same package.
 
         type notExported struct {}     //this struct is visible only in this package as it starts with small letter
         
         type Exported struct {         //variable starts with capital letter, so visible outside this package
             notExportedVariable int    //variable starts with small letter, so NOT visible outside package
             ExportedVariable int       //variable starts with capital letter, so visible outside package
             s string                   //not exported
             S string                   //exported
         }

Definition can be found [here](https://golang.org/ref/spec#Exported_identifiers), examples from [here]
(http://golangtutorials.blogspot.de/2011/06/structs-in-go-instead-of-classes-in.html)


# Goroutines, Channels and Mutex

## Concurrency vs Parallelism

Go is a concurrent language, multiple tasks are normally not executed side by side
in independent threads, but is rather switching between the different tasks. Often 
the two tasks are interdependent and need some for of communication between each
other to reach a final goal. Go reduces the amount of communication between the
multiple, interdependent tasks by using `goroutines` and `channels`.

goroutines can be started independently from one another. They can be coupled
to channels to enable interaction with the main program or other goroutines.
This way, a task can be broken down into subtasks, that can either be run concurrently, 
dependent on one another or properly in parallel.

Find a more detailed discussion [here](https://blog.golang.org/concurrency-is-not-parallelism).

"[...]

Concurrency is about dealing with a lots of things at once.

Parallelism is about doing lots of things at once.

[...]" [source](https://talks.golang.org/2012/waza.slide#8)


## Goroutine
- A goroutine is a thread managed by the Go runtime - it is like launching a function with shell's `&` notation.
- The execution of code within a goroutine happens parallel to any subsequent code after the routine has been started.
- When a goroutine blocks, it does not affect other goroutines.
- NOTE: Access to memory must be synchronized, if goroutines are used, since they run in the same address space!
- Example:

        func say(s string) {
            for i := 0; i < 10; i++ {
                time.Sleep(100 * time.Millisecond)
                fmt.Println(s)
            }
        }

        func main() {
            go say("world")
            say("hello")
        }


## Channel
- A channel is a typed sender and receiver of data. Channels can be used to communicate between `goroutines`.
- Values can be sent via a channel using the `<-` operator, information flows in the direction of the arrow.
- Channels have to be created using `make` before they can be used, e.g: `ch := make(chan int)`.
- Sends and receives block until the other side is ready.

        ch <- v     // send v to channel ch
        v := <-ch   // receive data from channel ch and assign value to v

- Example (adapted from [here](https://talks.golang.org/2012/waza.slide#33))

        // Communication channel
        timerChan := make(chan time.Time)

        // Start a goroutine that will start doing stuff immediately
        // and provide its result via the timerChan channel once its done
        go func() {
            time.Sleep(deltaT)
            timerChan <- time.Now() // finished, provide result via channel
        }

        fmt.Println("Do something")
        fmt.Println("in the meantime")
        fmt.Println("while we wait for the routine to finish")
        completedAt := <- timerChan // This receive will block at this point 
                                    // until the goroutine is done.
        fmt.Printf("Finished at '%s'", completedAt.Format())

- A single channel can be used by multiple goroutines as means to communicate.
These can be used to properly parallelize computation. Example adapted from [here](https://tour.golang.org/concurrency/2)

        func sum(s []int, c chan int) {
            sum := 0
            for _, v := range s {
                sum += v
            }
            c <- sum // send resulting sum to communication channel c
        }

        func main() {
            s := []int{7, 2, 8, -9, 4, 0}
    
            c := make(chan int)
            go sum(s[:len(s)/2], c)     // calculates 17
            go sum(s[len(s)/2:], c)     // calculates -5
            go sum(s, c)                // calculates 12
            x, y, z := <-c, <-c, <-c    // receive from c, blocks here until c has delivered for the third time.
    
            fmt.Println(x, y, z)    // returns 12 17 -5; if go sum(s, c) would be moved 
                                    // to the top of the routine list, 
                                    // it would return -5 12 17
        }

- NOTE: You must only consume as many channel results as the channel has been used in routines, 
otherwise a deadlock fatal error will occur!

### Buffered channel
- Channels can be created with a buffer to ensure, that not too many channels will be opened.

        ch := make(chan int, 2)
        ch <- 1
        ch <- 2             // adding ch <-3 here would lead to an error
        fmt.Println(<-ch)   // prints 1
        ch <- 3             // since one channel slot has been consumed, its ok to use it again
        fmt.Println(<-ch)   // prints 2
        fmt.Println(<-ch)   // prints 3

    
## Channel close and range
- A sender can close a channel. A receiver can test on his end, if a channel is still open.

        // sender:
        close(ch)
        // receiver
        v, ok := <-ch   // if the channel has been closed on the sender side, ok will be false.

- `range` in a loop will stop, if a channel has been closed.

        func fibonacci(n int, c chan int) {
            x, y := 0, 1
            for i := 0; i < n; i++ {
                c <- x
                x, y = y, x+y
            }
            close(c)
        }
    
        func main() {
            c := make(chan int, 10)
            fmt.Println(cap(c), "\n")
            go fibonacci(cap(c), c)
            for i := range c {          // range stops iterating, once c has been closed in the go routine
                fmt.Println(i)
            }
        }


## Mutex
- If goroutines are used but channels are not, Go provides a mutual exclusion mechanism to ensure, 
that variable access conflicts can be avoided.
- `sync.Mutex Lock` locks the access to a variable for everything outside the current goroutine
- `sync.Mutex Unlock` releases access to a locked variable 

## JSON Marshaling and Unmarshaling

Find a good introduction on this topic [here](https://www.dotnetperls.com/json-go).


# Tests
- Test files have to reside in the same package as the go files that are to be tested.
- Test files have the same name as the go files, with an additional "_test.go" ending.

        file.go
        file_test.go

- Run tests for all packages from the commandline using
 
        go test ./...
        
- Run tests with more detailed information

        go test -v ./...
        
- Run only tests where the name of the function matches regular expression

        go test -run="SomeFunctionNamePart" ./...

- Run only a specific test out of a specific package from the commandline, e.g. TestGetSSHKey of package data

        go test github.com/G-Node/gin-auth/data -run TestGetSSHKey


## Test driven development

- [Test-driven development with Go](https://leanpub.com/golang-tdd/read)


## Test Coverage

Go has really nice support for test coverage, find a detailed description in this 
[Go Blog article on coverage](https://blog.golang.org/cover). 

#### HTML coverage display

    go tool cover -html=count.out


# Go Web programming 

## Templates

`.` in a template accesses data structures that are passed to a template

    // passes in whole struct
    {{ . }}
    // accesses a field of a struct
    {{ .SomeField }}
    // accesses a method of a named type e.g. a method that returns a specific value from a DB
    {{ .SomeMethod }}


# Go initialization

Go programs are executed in the order:

- package-level variables
- init() function
- main() function

- if main imports dependencies,
    - each dependency is initialized
        - as first criteria if it is required by another
        - as second criteria in alphabetical order

                import {"a", "b", "c", "d"}
                // if "a" is dependent on "c" the initialization order would be "c", "a", "b", "d"
 
    - each dependency is initialized in the same order as above (1st package var, 2nd init func) 
    - after that package var, init fun, main func of the importing code.

Read the specs [here](https://golang.org/ref/spec#Program_initialization_and_execution)


# Go build process

- The go build toolchain:
    - go compiler, c compiler, assembler, linker
    - all of these can be found in go/src/cmd

## Building a go package

    // '-x' ... print build steps
    go build -x crypto/hmac

Building a go package does the following:
- create a temporary folder
- use the appropriate compiler for the current platform and the different source code files.
- pack the result to an archive

Note: 
- After a build the resulting archive is simply deleted when the temporary folder is deleted. 
- After an install, the created archive is copied to `GOPATH/pkg`.  
- Compiler and linker only accept a single file representing the built package. 
For this reason the archive is created during the build process using `pack`.

## Building a go command

- A go command is package which requires a file named `main.go` as entry point.
- The build process will perform additional steps to produce an executable.
- Building a command will leave the result in the current working directory.
- If `go install` is used, the resulting file fill be copied to `GOPATH/bin`.


Read more
- [Quickstart](https://golang.org/doc/code.html#Command)
- [How does the go build command work](http://dave.cheney.net/2013/10/15/how-does-the-go-build-command-work)


# Go Hands On

## Install Go
- check [Go Getting started](https://golang.org/doc/install) and install side by side with the following steps

- download latest zip from golang.org
- unpack to directory of choice e.g. `/usr/local` or in our case `$HOME/work/software`

       tar -C $HOME/work/software -xzf go$VERSION.$OS-$ARCH.tar.gz

- in case of `/usr/local` installation add to `/etc/profile`

       export PATH=$PATH:/usr/local/go/bin

- in case of custom path installation add to `$HOME/.profile` ... GOPATH is an additional directory, 
where go looks for installed packages

        export GOPATH=$HOME/work/software/go-packages
        export GOROOT=$HOME/work/software/go
        export PATH=$PATH:$GOROOT/bin
        export PATH=$PATH:$GOPATH/bin

- re-load `$PATH`

       source $HOME/.profile


## Install additional packages
- Move to the `$GOPATH` directory, in our case `$HOME/work/software/go-packages`
- There, run `go get [desired package]` e.g.

        go get github.com/golang/lint/golint


## Lint, vet and format your go code
To increase readability and enforce standard code layout go offers linting and autoformat.
So before checking in a file use the following lines of go code:

    fgt golint -min_confidence 0.9 ./...
    go vet ./...
    gofmt -w [yourfile].go

### gofmt
- `gofmt -d [filename]`     displays all changes that would be done to `filename` if it would be reformatted
- `gofmt -w [filename]`     automatically reformats `filename`
- `gofmt -w .`              automatically reformats all go files recursively from the current directory
- `goftm -l .`              lists all files that would be reformatted


## Tests
- `go test ./...`                   run tests for all packages in parallel (can lead to race conditions)
- `go test ./specificPackage`       run all tests of package `specificPackage`
- `go test -v ./...`                run all tests, be verbose about it
- `go test -p #x ./...`             run tests for all packages in parallel, but only #x packages at the same time
- `go test -p #1 ./...`             run all tests with only one package at a time

- for more information about go tests check the following
    [blog entry](https://splice.com/blog/lesser-known-features-go-test/).


## Third party package manager
- gopkg.in: install go packages not by go get but by version number of a github repo
    - find it [here](http://labix.org/gopkg.in)
    - [from here](http://stackoverflow.com/a/33948752)


## Logging with Go
- a description of how to use the standard go log can be found 
    [here](https://www.goinggo.net/2013/11/using-log-package-in-go.html)
- find an interesting view on logging [here](http://dave.cheney.net/2015/11/05/lets-talk-about-logging)
- logrus is a pretty interesting logger also providing support for hooks
    - find it [here](https://github.com/Sirupsen/logrus)
- support for logrotate with go by [NYTimes](https://github.com/NYTimes/logrotate)
    - a description about logrotate itself can be found [here](http://www.thegeekstuff.com/2010/07/logrotate-examples/)


## Go, QML and Qt
Some links about the topic: 
- [qml for go on github](https://github.com/go-qml/qml)
- [examples 1](http://blog.labix.org/2013/12/23/qml-components-with-go-and-opengl)
- [qml crashcourse](https://en.wikipedia.org/wiki/QML)

## Go and GTK

Another graphical user interface is GTK, find support and a nicely maintained GoTK3 project 
[here](https://github.com/gotk3/gotk3).

## Further nice to knows / reads
- Best practices for production environment: [Go in production](https://peter.bourgon.org/go-in-production/)
- Go common mistakes: [Code review comments](https://github.com/golang/go/wiki/CodeReviewComments)


## Go test coverage

- [How to create coverage for tests with Go](https://blog.golang.org/cover)

- create a file named `profile.cov` containing the coverage profile for the current go package:

        go test -coverprofile=profile.cov

- display which parts of code are covered by the tests and which are not, using the above created profile:

        go tool cover -html=profile.cov

- if there are more than one packages in a project, the cover profiles can be run and combined 
    using a custom bash script at the project root. 
    In this example `gin-repo` is the name of the project and has to be replaced with the actual project path.

        #!/bin/bash
        echo "mode: count" > profile.cov;
        for Dir in $(go list ./...);
        do
          # change path to actual project here
          currDir=$(echo $Dir | sed 's/github.com\/G-Node\/gin-repo\///g');
          currCount=$(ls -l $currDir/*.go 2>/dev/null | wc -l);
          if [ $currCount -gt 0 ];
          then
            go test -covermode=count -coverprofile=tmp.out $Dir;
            if [ -f tmp.out ];
            then
              cat tmp.out | grep -v "mode: count" >> profile.cov;
            fi
          fi
        done


## Go gotchas

### sqlx database get error with private fieldnames

- When using an sqlx database connection and handing over a struct for a get SELECT,
    the names of the struct fields have to be uppercase, otherwise an error will occur.

    - This error will also only occur, if the requested value is NOT STRING e.g. if it is int or bool.

            db, err = sqlx.Connect(dbDriver, openString)
            localStruct := &struct {
                blub int
            }{}
            q := `SELECT COUNT(blub) FROM sometable WHERE blub = $1`
            db.Get(localStruct, q, "somevalue")

            // Error: "sql: Scan error on column index 0: unsupported Scan, storing driver.Value type int64 
            // into type *struct { login int }"

    - if there are more than one struct fields the error message will change to

            localStruct := &struct {
                blub int
                blub2 bool
                blub3 int
            }{}
                ...
            // Error: "scannable dest type struct with >1 columns (3) in result"

    - it will only work, if the fieldnames of the struct are public (start with an uppercase letter)

            localStruct := &struct {
                // Uppercase here
                Blub int
            }{}
            q := `SELECT COUNT(blub) FROM sometable WHERE blub = $1`
            db.Get(localStruct, q, "somevalue")
            // works fine

- List of [Go Gotchas](http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/index.html#mline_lit_comma)
 with examples.

# Addendum

Distilled from resources:
- [Go homepage](https://golang.org/doc/)
- [Go by example](https://gobyexample.com/)
- [Go slices - usage and internals](http://blog.golang.org/go-slices-usage-and-internals)
- [Awesome Go](https://github.com/avelino/awesome-go)
- [Gonum: scientific go](https://github.com/gonum)
- [Go Jupyter notebooks](http://www.datadan.io/announcing-a-golang-kernel-for-jupyter-notebooks/)

Rehearse: Function: closures! Defer, Pointer section, Slices, Check how interfaces actually work!

## golang projects and libraries

- [image processing](https://github.com/anthonynsimon/bild)
- [go linter list](https://go.libhunt.com/project/go-tools-dominikh)
- [gonum - go scientific libraries](https://github.com/gonum)

## IDEs

- [Visual Studio code](https://code.visualstudio.com/)
- [Visual Studio code go extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.Go)
- [VS code go dubug extension](https://github.com/Microsoft/vscode-go/wiki/Debugging-Go-code-using-VS-Code)
