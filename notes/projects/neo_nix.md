## Current state of the neo-nixio

This is our goal for neo-nixio:

1. It should be feature-complete, that is, any data structure and data
type supported by Neo should be supported by the NIXIO for both
writing and reading.
2. All new features that are added to Neo should be available in the
NIXIO with minimal delay (preferably, before they are released
officially).
3. Writing a file to NIX from Neo and reading it back should have NO
information or structure loss and should make as few changes to the
data objects as possible.

The actual state is pretty close to the desired one.  The NIXIO
supports writing all types of Neo objects and preserves all their
annotations and properties, which are restored on load.  Most
structure changes and added features are added to the NIXIO shortly
after they become available (though there might be times when we
weren't as fast as we wanted to be).

Here's some issues that are currently open:
- Multi-dimensional annotations: Annotations are stored as metadata in
NIX and unfortunately, the NIX format only supports one-dimensional
arrays for metadata values.  We have some ideas for dealing with this
(either by upgrading the NIX format or by storing these annotations in
a different way), but as of right now the problem is still open.
- Empty annotations: Similar to above, though this one is easier to
solve.  There's a workaround solution currently in the NIXIO, but we
weren't satisfied with it so we're still thinking about it.
- The Neo-NIXIO can't read NIX files that were not created by the IO:
The Neo-NIXIO adds some metadata to the file when writing to make
restoring the original Neo structure possible when loading.  It may be
possible to partially support reading arbitrary NIX files in the
future, but there will always be compromises.  For now, the Neo-NIXIO
expects certain indicators that help it reconstruct the Neo objects
precisely.
- File size and write performance: Write performance was a bigger
issue in the past, but it has been (mostly) solved now.  There may be
a few minor optimisations that can be made.  File sizes are still
quite large, however.  This is a peculiar issue because it doesn't
come up in general NIX use, but it appears as a result of the data
structures that are common amongst Neo users and the requirements of
the IO.  Generally, when writing a Neo file to NIX, the NIXIO writes
some metadata per object to allow for lossless loading (loading back
the Neo structure without losing any information about its objects).
Unfortunately, these extra metadata objects add significant data
overhead per object, so Neo structures with large numbers of objects
(hundreds or SpikeTrains or Signals for instance) tend to create
unexpectedly large file sizes.

I should note that we are actively working on NIX and always keep in
mind how we can improve the Neo-NIXIO as well.  In terms of the
priorities we have for the IO (Neo feature completeness and keeping
data and metadata intact after write-read cycles), I feel the IO is
very mature.  I listed the issues above in the interest of full
transparency and openness.  Given your description of the data, I
can't imagine any of the limitations being an issue, but we can talk
in more detail if you have further questions.

