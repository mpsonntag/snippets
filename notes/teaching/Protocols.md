# Networking

IP ... internet protocol
inter network communication protocol to enable communication between
two defined addresses. IPv4 addresses.

UDP ... User datagram protocol
inter network data transfer protocol. carries besides the data itself only 
checksum and the address of the receiver. does not provide support against data loss.

Ports ... 
logical construct to enable multiple different gate points at a specific address
for different services. can also be seen as an endpoint of a communication 
channel. at an endpoint 16bit unsigned integer number of ports can be
assigned, ranging 0-65535. Depending on the protocol ports may be reserved and
should not be used e.g. port 0 for TCP

TCP ... Transmission control protocol


DAV

WebDAV

SMTP

HTTP

HTTPS

TLS

SSH


TTY ... teletypewriter - driver to provide connection between kernel and a shell
"In unix terminology, a tty is a particular kind of device file which implements a 
number of additional commands (ioctls) beyond read and write. In its most common meaning, 
terminal is synonymous with tty." [from here](https://unix.stackexchange.com/a/4132)

A tty provides session management, program handling (signals for starting, stopping, 
killing of processes, etc; e.g. SIGTERM, SIGKILL, ... when an application stops, the 
SIGTERM is used), IO operations in the shell ("line disciplines") and terminal display 
handling e.g. vim file content display.

[tty introduction](http://www.linusakesson.net/programming/tty/index.php)
