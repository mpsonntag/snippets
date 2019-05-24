# Notes on bash scripting

#### shebang line

The shebang line for executable scripts should start with `#!/usr/env/bin bash`
to make it system independent. For more infos see [this discussion](
https://stackoverflow.com/questions/10376206/what-is-the-preferred-bash-shebang).

#### Setting the environment of a script

Use `set -eu` to end a script prematurely when an error occurs.

