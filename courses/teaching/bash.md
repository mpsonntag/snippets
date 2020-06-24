# Notes on bash scripting

#### shebang line

The shebang line for executable scripts should start with `#!/usr/env/bin bash`
to make it system independent. For more infos see [this discussion](
https://stackoverflow.com/questions/10376206/what-is-the-preferred-bash-shebang).

#### Setting the environment of a script

Use `set -eu` to end a script prematurely when an error occurs.

#### Parenthesis

- `[` is a synonym for the shell command `test` and in the `[]` form can be used in 
  script conditionals in almost all shells beside bash.
- `[[]]` is a bash specific version of `test` with additional features.
- `()` opens a subshell. Can be used to run commands without affecting the main shell.
- `${}` unambiguously identifies variables in a script
- `{}` can be used to execute a sequence of commands in the current shell

Check here for details:
- [BASH FAQ](
  http://mywiki.wooledge.org/BashFAQ/031
  )
- [Notes on brackets](
  https://stackoverflow.com/questions/2188199/how-to-use-double-or-single-brackets-parentheses-curly-braces
  )


### Various script lines

#### Check whether a user is in a specific group

    # check if user 'fuseki' is in group 'docker'
    VAR=$(id fuseki | grep docker)
    test -z $VAR && echo "empty" || echo $VAR
